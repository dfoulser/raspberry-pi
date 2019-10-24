# Code to read Mic + ADC data from I2C bus and write it out to 
# files based on filename prefix.  Use file rolling per minute.
# Import the ADS1x15 module.
import Adafruit_ADS1x15
import argparse
import numpy as np
# Import the sound library for read/write WAV files (also compressed MP3)
import soundfile

int SAMPLE_RATE = 3300  # 3300 Hz is fastest the ADS1015 can read
int DURATION_SECONDS = 60  # one minutes
int CHANNEL = 0  # wire all devices to A0 channel
int NUM_DEVICES = 1  # working with a single ADC now, later read this from the hardware itself
str SOUNDFILE_PATTERN = "%s_%4d%2d%2d_%02d%02d.wav"

def handleArgs():
    parser = argparse.ArgumentParser(description='Record data from Mic+ADC.')
    parser.add_argument('filename', metavar='prefix', type=str, 
        help='write files to prefix_YYYYMMDD_HHmm.wav')
    parser.add_argument('--duration_mins', dest='duration', action='store_const',
        const=sum, default=1, help='duration of sampling in minutes')

    args = parser.parse_args()
    return args

def allocateSamplesArray():
    array = np.zeros((NUM_DEVICES, SAMPLE_RATE * DURATION_SECONDS), dtype=int16 )
    # Channels of sound are stored as rows in 2D numpy array.  Each
    # channel comes from one of the ADC devices.
    return array

def setupAdc():
    # Create an ADS1015 ADC (12-bit) instance.
    # Set the I2C address as its default (0x48), and the I2C
    # bus number as 1 (0 is default):
    ### When using >1 devices, use an array of addresses per ADS1015 specs.
    adc = Adafruit_ADS1x15.ADS1015(address=0x48, busnum=1)
    # Choose a gain of 1 for reading voltages from 0 to 4.09V.
    # Or pick a different gain to change the range of voltages that are read:
    #  - 2/3 = +/-6.144V
    #  -   1 = +/-4.096V
    #  -   2 = +/-2.048V
    #  -   4 = +/-1.024V
    #  -   8 = +/-0.512V
    #  -  16 = +/-0.256V
    # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
    GAIN = 2

    # Data rate goes up to 3300 with ADS1015. Default is 1600.
    DATA_RATE = SAMPLE_RATE

    # Start continuous ADC conversions on selected channel using the previously set gain
    # value.  Note you can also pass an optional data_rate parameter, see the simpletest.py
    # example and read_adc function for more infromation.
    adc.start_adc(CHANNEL, gain=GAIN, data_rate=DATA_RATE)
    # Once continuous ADC conversions are started you can call get_last_result() to
    # retrieve the latest result, or stop_adc() to stop conversions.
    return adc

def stopAdc(adc):
    # Stop continuous conversion.  After this point you can't get data from get_last_result!
    adc.stop_adc()

def readData(adcs, samplesArray, data_rate=DATA_RATE, duration=DURATION_SECONDS):
    print('Reading %d ADS1015 channel 0 for %d seconds...', adcs.shape()[0], duration)
    start = time.time()
    timeStamp = start
    sample = 0
    SAMPLE_COUNT = duration * data_rate
    interval = 1.0/DATA_RATE
    while sample < SAMPLE_COUNT && timeStamp < (start + interval * SAMPLE_COUNT):
        for i in range(adcs.shape()[0]):
            # Read the last ADC conversion value and save it.
            samplesArray[i, sample] = adcs[i].get_last_result()
        # WARNING! If you try to read any other channel of this ADC during this continuous
        # conversion (like by calling read_adc again) it will disable the
        # continuous conversion!
        # print('Channel 0: {0}'.format(value))
        # Sleep for rest of the interval (until next timeStamp)
        sample = sample + 1
        timeStamp = timeStamp + interval
        time.sleep(timeStamp - time.time())

def getDatetimeFilename(prefix):
    timeStamp = time.time()
    filename = prefix + timeStamp.strftime('_%Y%m%d_%H%M.wav')
    return filename


def main():
    args = handleArgs()
    adcs = []
    for i in range(NUM_DEVICES):
        adcs[i] = setupAdc()
    samplesArray = allocateSamplesArray()
    # Read the data
    readData(adcs, samplesArray)
    # Write the array of samples as sound file
    filename = getDatetimeFilename(args.filename)
    soundfile.write(filename, samplesArray, DATA_RATE)
    # Close the ADCs
    for i in range(NUM_DEVICES):
        stopAdc(adc[i])
    print("Done")


if __name__ == '__main__':
    main()
