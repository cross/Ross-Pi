#!/usr/bin/python
# vim: set fileencoding=utf-8 :
#
# Based on AdafruitDHT.py
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import os
import argparse

import Adafruit_DHT

# Parse command line parameters.
parser = argparse.ArgumentParser(description='Report and/or submit temperature and humidity.')
parser.add_argument('-F', dest='format', action='store_const',
		    const='F', default='C',
		    help='temperature in Fahrenheit (default: Celsius)')
parser.add_argument('sensor', type=str, choices=['11', '22', '2302'],
		    help='type of sensor')
parser.add_argument('pin', type=int, choices=range(1, 31), metavar='<1-31>',
		    help='GPIO PIM number')

sensor_vals = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

args = parser.parse_args()

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = (None, None)
try:
    humidity, temperature = Adafruit_DHT.read_retry(sensor_vals[args.sensor], args.pin)
except RuntimeError as e:
    if os.geteuid() > 0:
        print("RuntimeError (%s): Perhaps you need to be root?" % e)
    else:
        print("RuntimeError (%s)" % e)
    sys.exit(2)
except ValueError as e:
    print("ValueError: %s" % e)
    sys.exit(3)
except Exception as e:
    print(e)
    sys.exit(4)

temperatureF = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
if humidity is not None and temperature is not None:
    if args.format == 'F':
	print('Temp={0:0.1f}°F  Humidity={1:0.1f}%'.format(temperatureF, humidity))
    else:
	print('Temp={0:0.1f}°C  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)
