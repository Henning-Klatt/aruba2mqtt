import paho.mqtt.client as mqtt
import json
import logging
import time

# ToDo: https://stackoverflow.com/a/77985329
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "aruba2mqtt")

def connect(mqtt_host):
    reconnect_delay = 1
    while True:
        try:
            client.connect(mqtt_host)
            logging.info("MQTT Connected successfully!")
            return
        except Exception as err:
            logging.error("%s. MQTT Connecting to %s failed.", err, mqtt_host)
            reconnect_delay *= 2
            reconnect_delay = min(reconnect_delay, 60)
            logging.info("Retrying in %d seconds...", reconnect_delay)
            time.sleep(reconnect_delay)

def publish(device):
    data = {
        "mac": device.mac,
        "rssi": device.rssi,
        "temperature": device.temp,
        "humidity": device.humi,
        "battery" : device.battery
    }
    client.publish("aruba2mqtt/" + device.name + "/state", json.dumps(data))

def send_discovery(device):

    _config = {
        "name": f"{device.name} Temperature",
        "state_topic": f"aruba2mqtt/{device.name}/temp",
        "unit_of_measurement": "°C",
        "device_class": "temperature",
        "device": {
            "identifiers": device.name,
            "name": device.name,
            "model": "ATC",
            "manufacturer": "Xiaomi"
        }
    }

    discovery_prefix = "homeassistant"
    node_id = device.name
    object_id = "temp"
    payload = json.dumps(_config)
    client.publish(discovery_prefix + "/sensor/" + node_id + "/" + object_id + "/config", payload)

    _config = {
        "name": f"{device.name} Humidity",
        "state_topic": f"aruba2mqtt/{device.name}/humi",
        "unit_of_measurement": "%",
        "device_class": "humidity",
        "device": {
            "identifiers": device.name,
            "name": device.name,
            "model": "ATC",
            "manufacturer": "Xiaomi"
        }
    }
    object_id = "humi"
    payload = json.dumps(_config)
    client.publish(discovery_prefix + "/sensor/" + node_id + "/" + object_id + "/config", payload)
