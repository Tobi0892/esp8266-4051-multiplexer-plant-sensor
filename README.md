# ESP8266 Multi Capacitive Soil Moisture Sensor

ESP8266 in combination with a eight port multiplexer to **support up to 8 capacitive soil moisture sensors**.

The esp8266 reads the sensors every 10 minutes, transfers the readings via MQTT to a broker and goes back to deep sleep. The MQTT messages and can be picked up by i.e. Home Assistant.

- Mode 1: USB powered
- Mode 2: Battery powered (optional solar)

The code is written in **MicroPython**.

## Mode 1: USB powered

### Parts required

- [Wemos D1 mini Pro V2.0.0 ESP8266](https://www.aliexpress.com/item/32724692514.html) 4,56€
- [Capacitive soil moisture sensor](https://www.aliexpress.com/item/32863717622.html) 0,61€
- [CD4051 Multiplexer](https://www.aliexpress.com/item/32424603555.html) 1,85€
- [Project box](https://www.aliexpress.com/item/4000392100897.html) 0,72€
- [Circuit board](https://www.aliexpress.com/item/1848518580.html) 1,66€
- [Wires](https://www.aliexpress.com/item/4000329909050.html) 1,90€
- [Pin headers](https://www.aliexpress.com/item/32861400498.html) 0,88€

A usb charger and micro usb cable is assumed to be available.

### Circuit diagram

![mode 1 wiring](circuit%20drawings/usb_powered.JPG)

## Mode 2: Battery powered

Use more batteries in parallel if you want (a) to decrease the time between sensor readings or (b) prolong the time until the next charging cycle or (c) compensate for smaller solar panels.

The solar panel is optional, of course you can also charge the batteries manually with a charger once they are drained. If you use a solar panel, you need to connect it via the micro usb port to the esp8266

Note: the Wemos D1 mini Pro v2.0.0 already has a built-in charging module. 

### Additional parts required

- [18650 3,7V 3400mAh battery](https://www.aliexpress.com/item/33016517000.html) 2,21€
- [JST connector](https://www.aliexpress.com/item/33027366342.html) 0,49€
- [Optinal 5V 5W solar panel](https://www.aliexpress.com/item/32952130996.html) 4,13€

### Circuit diagram

![mode 2 wiring](circuit%20drawings/battery_powered.JPG)

## Setup

### Configuration

Use the `config.json` to configure the esp8266 (no changes in `boot.py` or `main.py` required).

```json
{
  "hostname": "NAME_OF_ESP8266",
  "wifi": {
    "ssid": "YOUR_WIFI_NAME",
    "password": "YOUR_WIFI_PASSWORD",
  },
  "mqtt": {
    "user": "MQTT_USER",
    "password": "MQTT_PASSWORD",
    "broker": "MQTT_BROKER_IP",
    "port": 1883,
    "topics": "TOPIC_NAME"
  }
}
```

### Flashing Code to ESP8266

I prefer PyCharm and the respective [MicroPython plugin](https://blog.jetbrains.com/pycharm/2018/01/micropython-plugin-for-pycharm/). Nevertheless, you can use any other suitable editor.

Create a configuration for each of the three files and flash them onto the esp8266. You can use the MicroPython REPL to watch the execution of the programs:

```
Connecting to WiFi...connected
Connecting to MQTT...connected
Sending: {"analog": "481", "percent": "7", "updated": "07.02.2020 23:12:25"} 
Going back to sleep...
```

### Home Assistant

Add i.e. two mqtt sensors to your `sensors.yaml` (your one esp8266 published to both topics as it operates multiple soil moisture sensors)

```yaml
- platform: mqtt
  name: "Ikea Bäumchen"
  state_topic: "esp8266/pflanzen-wohnzimmer-fenster/sensor0"
  value_template: "{{ value_json.percent }}"
  unit_of_measurement: "%"
  json_attributes_topic: "esp8266/pflanzen-wohnzimmer-fenster/sensor0"
  icon: mdi:sprout
- platform: mqtt
  name: "Zitronenbaum"
  state_topic: "esp8266/pflanzen-wohnzimmer-fenster/sensor1"
  value_template: "{{ value_json.percent }}"
  unit_of_measurement: "%"
  json_attributes_topic: "esp8266/pflanzen-wohnzimmer-fenster/sensor1"
  icon: mdi:sprout
```

And the following to `ui-lovelace.yaml` to display the two sensors in the lovelace frontend ([Custom multiple entities card is used in this example](https://github.com/benct/lovelace-multiple-entity-row))

```yaml
  - type: markdown
    style: !include /config/ui-lovelace/style/title.yaml
    content: Pflanzen

  - type: entities
    entities:
      - type: custom:multiple-entity-row
        entity: sensor.ikea_baumchen
        name: IKEA Bäumchen
        hide_state: true
        primary:
          entity: sensor.ikea_baumchen
          attribute: analog
          unit: ''
          name: 'Analog'
        secondary:
          entity: sensor.ikea_baumchen
          attribute: percent
          name: 'Wasser'
          unit: '%'
      - entity: sensor.zitronenbaum
        name: Zitronenbaum
        hide_state: true
        type: custom:multiple-entity-row
        primary:
          entity: sensor.zitronenbaum
          attribute: analog
          unit: ''
          name: 'Analog'
        secondary:
          entity: sensor.zitronenbaum
          attribute: percent
          unit: '%'
          name: 'Wasser'
```

Result:

![lovelace](build%20pictures/homeassistant.png)

## Schematics

- [Wemos D1 mini pro](https://wiki.wemos.cc/products:d1:d1_mini_pro)
- [CD4051 Multiplexer](http://www.ti.com/lit/ds/schs047i/schs047i.pdf)

## Build pictures
Two sensors placed in a plant each (maybe add a 3D printed sensor cover?)
![sensors](build%20pictures/sensors.jpg)

Three sensors connected to the esp (3 more available - multiplexer supports up to 8)
![sensors_connected](build%20pictures/sensors_connected.jpg)

Front view of the connectors (the wholes could have been drilled better)
![front](build%20pictures/front.jpg)

Micro usb power connected
![power](build%20pictures/power.jpg)

VCC and GND JST connectors glued in place
![all_inputs](build%20pictures/all_inputs.jpg)

6 analog pins (multiplexer channels) for 6 soil moisture sensors glued in place
![analog pins](build%20pictures/analog_pins.jpg)

Case prepared
![Case](build%20pictures/case.jpg)

Mode 1 completed without case and ability to connect 4 moisture sensors (2 more have been added after taking the picture)
![Mode one completed without case](build%20pictures/mode_one_completed_without_case.jpg)

Sleep pin soldered to be able to wake up from deep sleep
![Sleep Pin soldered](build%20pictures/sleep_pin_soldered.jpg)

Wiring below esp8266 (not all connections are visible from the top)
![Wiring](build%20pictures/wiring.jpg)

Back with soldered connections
![Back](build%20pictures/back.jpg)

Multiplexer wired to headers for esp8266 without connectors for sensors
![multiplexer](build%20pictures/multiplexer.jpg)

Back of esp8266 and multiplexer wiring
![back_plain](build%20pictures/back_plain.jpg)

Capacitive soil moisture sensors protected with hot glue
![soil front](build%20pictures/soil_front.jpg)

Also pins at back are protected 
![soil_back](build%20pictures/soil_back.jpg)