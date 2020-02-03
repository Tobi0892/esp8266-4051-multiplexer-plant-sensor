from machine import Pin, ADC
import json
from time import sleep

adc = ADC(0)

pinA = Pin(12, Pin.OUT)
pinB = Pin(13, Pin.OUT)
pinC = Pin(14, Pin.OUT)


def setMultiplexerPins(a, b, c):
    pinA.value(a)
    pinB.value(b)
    pinC.value(c)


def readSensors():

    sensors = {}

    i = 0
    while i < 8:
        # Convert sensor number to binary in order to set sensor input of multiplexer
        args = list("{0:03b}".format(i))
        setMultiplexerPins(int(args[0]), int(args[1]), int(args[2]))

        # Read sensor value
        sensorAnalog = adc.read()
        if sensorAnalog < 10:
            sensors["sensor" + str(i)] = {
                "state": "off",
                "analog": "",
                "percent": ""
            }
        else:
            wetPlant = 250 # water 200
            dryPlant = 500 # air 700
            sensorPercent = int((1 - (sensorAnalog - wetPlant) / (dryPlant - wetPlant)) * 100)

            if sensorPercent > 100:
                sensorPercent = 100
            elif sensorPercent < 0:
                sensorPercent = 0

            sensors["sensor" + str(i)] = {
                "state": "on",
                "analog": sensorAnalog,
                "percent": sensorPercent
            }

        i += 1

    return sensors


while True:
    sensors = readSensors()
    print(json.dumps(sensors))
    sleep(3)
