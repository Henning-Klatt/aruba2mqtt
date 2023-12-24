#!/usr/bin/env python

import logging
from websockets.sync import server
from google.protobuf.json_format import MessageToJson

import aruba_iot_nb_ble_data_pb2
import aruba_iot_nb_pb2

from Device import ATC
import mqtt

logging.basicConfig(format='%(asctime)s - %(message)s', level="INFO")

aruba_telemetry_proto = aruba_iot_nb_pb2.Telemetry()

# List of discovered BLE devices
devices = []

def getDevice(mac):
    for device in devices:
        if device.mac == mac:
            return device
    return None

def handle_aruba_telemetry_proto_mesg(mesg):
    try:
        aruba_telemetry_proto.ParseFromString(mesg)
        logging.debug(MessageToJson(aruba_telemetry_proto))

        logging.debug("Reporter: %s (%s)", aruba_telemetry_proto.reporter.name, aruba_telemetry_proto.reporter.mac.hex(":"))

        for blepacket in aruba_telemetry_proto.bleData:
            mac = blepacket.mac.hex(":")

            dev = getDevice(mac)
            if dev is None:
                return

            if blepacket.frameType == aruba_iot_nb_ble_data_pb2.BleFrameType.adv_ind:
                logging.debug("Got data: %s", blepacket.data.hex())
                dev.parse_payload(bytes(bytearray(blepacket.data)))
                dev.rssi = blepacket.rssi
                if(dev.temp != None and dev.humi != None):
                    logging.info("[%s] Temperature: %s °C | Humidity: %s %% | RSSI: %s | Battery: %s %%", dev.name, dev.temp, dev.humi,
                                 dev.rssi, dev.battery)
                    mqtt.publish(dev)
            if blepacket.frameType == aruba_iot_nb_ble_data_pb2.BleFrameType.scan_rsp:
                logging.debug("Found Device: %s (%s)", blepacket.data.decode("utf-8"), mac)

        for scanned_device in aruba_telemetry_proto.reported:
            mac = scanned_device.mac.hex(":")
            name = scanned_device.localName

            if not any(device.mac == mac for device in devices):
                dev = ATC(mac, name)
                devices.append(dev)
                logging.info("Added Device: %s (%s)", name, mac)
                if dev.name.startswith("ATC_"):
                    # Not working
                    #mqtt.send_discovery(dev)
                    pass

    except Exception as e:
        logging.error(e)

def receive(websocket):
    for message in websocket:
        if(isinstance(message, str)):
            logging.info("Got string: %s", message)
        else:
            handle_aruba_telemetry_proto_mesg(message)

def main():
    mqtt.connect()
    with server.serve(receive, "0.0.0.0", 7443) as websock:
        websock.serve_forever()


if __name__ == '__main__':
    main()
