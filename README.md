# mqtt2lcdd
Small python script that reads values from a mqtt broker and puts them on a 16x2 Character LCD using lcdproc. Used for displaying temperature levels from my heating system.
Makes use of the following:
* [Adafruit Blue&White 16x2 LCD+Keypad Kit for Raspberry Pi](https://www.adafruit.com/product/1115)
* [lcdproc](https://github.com/lcdproc/lcdproc). A client/server suite for controlling a wide variety of LCD devices 
* [pylcddc](https://pypi.org/project/pylcddc/). A python library for interfacing with LCDd, the server component of the commonly known LCDproc
* [Mosquitto MQTT broker](https://mosquitto.org/)
* [hometop_HT3](https://github.com/norberts1/hometop_HT3). Used for reading various values from my heaters system-bus and sending them to the MQTT broker
