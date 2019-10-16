# Code to read Mic + ADC data from I2C bus and write it out to 
# files based on filename prefix.  Use file rolling per minute.
import argparse

def handleArgs():
    parser = argparse.ArgumentParser(description='Record data from Mic+ADC.')
    parser.add_argument('filename', metavar='prefix', type=str, 
        help='write files to prefix_HHMM.csv')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #     const=sum, default=max, help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.filename))

def main():
    handleArgs()


if __name__ == '__main__':
    main()
