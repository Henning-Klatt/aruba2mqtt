#!/usr/bin/env python

import logging
import jsonpickle
from pprint import pprint
from websockets.sync import server

import aruba_iot_nb_ble_data_pb2
import parse
from google.protobuf.json_format import MessageToJson

import aruba_iot_nb_pb2

logging.basicConfig(format='%(asctime)s - %(message)s', level="INFO")

aruba_telemetry_proto = aruba_iot_nb_pb2.Telemetry()
def handle_aruba_telemetry_proto_mesg(mesg):
    try:
        aruba_telemetry_proto.ParseFromString(mesg)
        logging.info(MessageToJson(aruba_telemetry_proto))

        logging.info("Reporter: %s (%s)", aruba_telemetry_proto.reporter.name, aruba_telemetry_proto.reporter.mac.hex(":"))

        for blepacket in aruba_telemetry_proto.bleData:
            mac = blepacket.mac.hex(":")
            if blepacket.frameType == aruba_iot_nb_ble_data_pb2.BleFrameType.adv_ind:
                result = parse.parse_payload(mac, blepacket.rssi, bytes(bytearray(blepacket.data)))
                logging.info(result)
            if blepacket.frameType == aruba_iot_nb_ble_data_pb2.BleFrameType.scan_rsp:
                logging.info("Found Device: %s (%s)", blepacket.data.decode("utf-8"), mac)

    except Exception as e:
        logging.error(e)

def receive(websocket):
    for message in websocket:
        if(isinstance(message, str)):
            logging.info("Got string: %s", message)
        else:
            handle_aruba_telemetry_proto_mesg(message)

def main():
    with server.serve(receive, "0.0.0.0", 7443) as websock:
        websock.serve_forever()


if __name__ == '__main__':
    main()
