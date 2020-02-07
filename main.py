from json import load, dumps
from time import sleep

from machine import Pin, ADC, RTC, deepsleep, DEEPSLEEP
from umqtt.simple import MQTTClient

with open("config.json", "r") as config:
    config = load(config)

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
        if sensorAnalog >= 50:
            wetPlant = 250 # water 200
            dryPlant = 500 # air 700
            sensorPercent = int((1 - (sensorAnalog - wetPlant) / (dryPlant - wetPlant)) * 100)

            if sensorPercent > 100:
                sensorPercent = 100
            elif sensorPercent < 0:
                sensorPercent = 0

            updated = RTC().datetime()

            sensors["sensor" + str(i)] = {
                "analog": sensorAnalog,
                "percent": sensorPercent,
                "updated": "{:02d}.{:02d}.{:02d} {:02d}:{:02d}:{:02d}".format(updated[2], updated[1], updated[0], int(updated[4]) + 1, updated[5], updated[6])
            }

        i += 1

    return sensors


def connectMQTT():
    print("Connecting to MQTT...", end="")

    mqtt = MQTTClient(
        config["hostname"],
        config["mqtt"]["broker"],
        user=config["mqtt"]["user"],
        password=config["mqtt"]["password"],
        port=config["mqtt"]["port"]
    )

    mqtt.connect()
    print("connected")
    return mqtt


###### MAIN ######

# Read sensors
sensors = readSensors()

# Send result via mqtt
mqtt = connectMQTT()

for sensor, data in sensors.items():
    print("Sending: " + dumps(data))
    mqtt.publish(
        config["mqtt"]["topics"] + "/" + config["hostname"] + "/" + sensor,
        dumps(data)
    )

# Wait for message(s) to be published
sleep(3)
mqtt.disconnect()

# Enter next cycle for 10 minutes deep sleep
print("Going back to sleep...")
rtc = RTC()
rtc.irq(trigger=rtc.ALARM0, wake=DEEPSLEEP)
rtc.alarm(rtc.ALARM0, 600000)
deepsleep()
