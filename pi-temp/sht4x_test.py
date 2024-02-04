#!/usr/bin/env python3
# vim: set fileencoding=utf-8 sts=4 sw=4 et:

import sys
import time
from datetime import datetime
import board
import busio
import adafruit_sht4x
from pprint import pprint

nattempts=5
for i in range(nattempts):
    try:
        i2cthingy = board.I2C()
        sht = adafruit_sht4x.SHT4x(i2cthingy)
        #pprint(sht)
    except OSError as e:
        print("Got OSError {}, what to do....".format(e.errno))
        time.sleep(0.25)
    except Exception as e:
        print(f"Got an exception: {e}")
        time.sleep(0.25)
    else:
        break

if 'sht' not in locals() or not sht:
    print("Unable to open SHT4x i2c interface, exiting.")
    sys.exit(2)

print("Found SHT4x with serial number", hex(sht.serial_number))

sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
# Can also set the mode to enable heater
# sht.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
print("Current mode is: ", adafruit_sht4x.Mode.string[sht.mode])

while True:
    try:
        temperature, relative_humidity = sht.measurements
    except (OSError,RuntimeError) as e:
        # We seem to get a couple of exceptions, for unknown reasons.
        #   OSError: [Errno 121] Remote I/O error
        #   RuntimeError: Invalid CRC calculated
        # But, they're unpredictable, so if we see these expected ones,
        # just try again.
        if "Remote I/O error" in str(e) or \
           "Invalid CRC calculated" in str(e):
            time.sleep(0.1)
            continue
        else:
            print("{}: {}".format(type(e).__name__,e))
            raise
    except Exception as e:
        print(f"Got exception: {e}")
        time.sleep(0.25)
        raise
#    print(datetime.now())
    print("Temp=%0.1f*C  Humidity=%0.1f%%" % (temperature,relative_humidity))
#    print("")
    time.sleep(5)
