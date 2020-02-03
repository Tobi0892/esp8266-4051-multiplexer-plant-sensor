import network
import machine
import gc
import time
import json

gc.collect()

with open('config.json', 'r') as config:
    config = json.load(config)


def connectWifi():
    wifi = network.WLAN(network.STA_IF)
    if not wifi.isconnected():
        print('connecting to network...')
        wifi.config(essid=config["wifi"]["hostname"], dhcp_hostname=config["wifi"]["hostname"])
        wifi.active(True)
        wifi.connect(config["wifi"]["ssid"], config["wifi"]["password"])
        while not wifi.isconnected():
            pass


try:
    connectWifi()
except(RuntimeError, TypeError, NameError):
    time.sleep(60)
    machine.reset()
