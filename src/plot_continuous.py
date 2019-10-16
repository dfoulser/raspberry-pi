# Simple demo of continuous ADC conversion mode for channel 0 of the 
# ADS1x15 ADC.
# Author: Tony DiCola
# License: Public Domain
#
# Update 2019-10-16 by Dave Foulser to read the ADS1015 (12-bit) for 5 sec
# and use matplotlib to draw a plot of the captured data.
import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15

# Import plotting libraries as well.
#import backports.functools_lru_cache as lru_cache
import matplotlib.pyplot as plt
import numpy as np

# Create an ADS1115 ADC (16-bit) instance.
#adc = Adafruit_ADS1x15.ADS1115()

# Or create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
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
GAIN = 1

# Data rate goes up to 3300 with ADS1015. Default is 1600.
DATA_RATE = 3300

# Start continuous ADC conversions on channel 0 using the previously set gain
# value.  Note you can also pass an optional data_rate parameter, see the simpletest.py
# example and read_adc function for more infromation.
adc.start_adc(0, gain=GAIN, data_rate=DATA_RATE)
# Once continuous ADC conversions are started you can call get_last_result() to
# retrieve the latest result, or stop_adc() to stop conversions.

# Note you can also call start_adc_difference() to take continuous differential
# readings.  See the read_adc_difference() function in differential.py for more
# information and parameter description.

# Read channel 0 for 5 seconds and print out its values.
print('Reading ADS1x15 channel 0 for 5 seconds...')
start = time.time()
values = {}
i=0
while (time.time() - start) <= 5.0:
    # Read the last ADC conversion value and print it out.
    value = adc.get_last_result()
    values[i] = value
    i = i + 1
    # WARNING! If you try to read any other ADC channel during this continuous
    # conversion (like by calling read_adc again) it will disable the
    # continuous conversion!
    # print('Channel 0: {0}'.format(value))
    # Sleep for half a second.
    # time.sleep(0.5)

# Stop continuous conversion.  After this point you can't get data from get_last_result!
adc.stop_adc()

# Draw the plot.
n = len(values)
v = np.zeros(n)

for i in range(n):
  v[i] = values[i]

fig, ax = plt.subplots()

print("Len(values)")
print(len(values))

ax.plot(v)
plt.show()


