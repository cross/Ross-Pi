# pi-temp

Originally written in 2016, this uses the Adafruit DHT library (which needs
to be installed on the system) to talk to a DHT temp/humidity sensor.

Based on original code from Adafruit (AdafruitDHT.py here), ross_pi0w_temp
will read from a sensor of a particular type connected to a particular GPIO
pin.  Above the original code, we added the ablity to loop, and the ability
to report data to a carbon/graphite server.  This allowed us to use grafana
as a front-end.
