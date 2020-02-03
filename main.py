import machine
from time import sleep

adc = machine.ADC(0)

pinA = machine.Pin(12, machine.Pin.OUT)
pinB = machine.Pin(13, machine.Pin.OUT)
pinC = machine.Pin(14, machine.Pin.OUT)


def setMultiplexerPins(a, b, c):
    pinA.value(a)
    pinB.value(b)
    pinC.value(c)


def setMultiplexerSensor(sensor):
    switcher = {
        0: setMultiplexerPins(0, 0, 0),
        1: setMultiplexerPins(0, 0, 1),
        2: setMultiplexerPins(0, 1, 0),
        3: setMultiplexerPins(0, 1, 1),
        4: setMultiplexerPins(1, 0, 0),
        5: setMultiplexerPins(1, 0, 1),
        6: setMultiplexerPins(1, 1, 0),
        7: setMultiplexerPins(1, 1, 1)
    }

    return switcher.get(sensor)


def getSensorValue(sensor):
    setMultiplexerSensor(sensor)
    SoilMoistVal = adc.read()
    # SoilMoistVal = (((1 / adc.read()) * 1000) / 0.0130027799046692741206740751471) - 101

    # if SoilMoistVal > 100:
    #     SoilMoistVal = 100
    # if SoilMoistVal < 0:
    #     SoilMoistVal = 0

    return SoilMoistVal


while True:
    print(getSensorValue(0))
    sleep(1)
