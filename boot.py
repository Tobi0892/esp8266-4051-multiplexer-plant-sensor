import gc
import json
from time import sleep

import esp
import network
from machine import reset

esp.osdebug(None)
gc.collect()

with open("config.json", "r") as config:
    config = json.load(config)


def connectWifi():
    wifi = network.WLAN(network.STA_IF)
    print("")
    print("Connecting to WiFi...", end="")

    wifi.config(
        essid=config["hostname"],
        dhcp_hostname=config["hostname"]
    )

    wifi.active(True)

    wifi.connect(
        config["wifi"]["ssid"],
        config["wifi"]["password"]
    )

    while not wifi.isconnected():
        pass

    print("connected")


try:
    connectWifi()

except(RuntimeError, TypeError, NameError):
    sleep(60)
    reset()
