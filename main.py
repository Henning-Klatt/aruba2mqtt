#!/usr/bin/env python

import logging
import jsonpickle
from websockets.sync import server
import parse

import aruba_iot_nb_pb2

logging.basicConfig(format='%(asctime)s - %(message)s', level="INFO")

aruba_telemetry_proto = aruba_iot_nb_pb2.Telemetry()
def handle_aruba_telemetry_proto_mesg(mesg):
    try:
        aruba_telemetry_proto.ParseFromString(mesg)
        logging.info(jsonpickle.encode(aruba_telemetry_proto.meta))
        logging.info(jsonpickle.encode(aruba_telemetry_proto.reporter))
        logging.info(jsonpickle.encode(aruba_telemetry_proto.bleData))

        if(aruba_telemetry_proto.bleData.frameType == "adv_ind"):
            result = parse.parse_payload("", -94, aruba_telemetry_proto.bleData.data)
            print(result)
        else:
            print(aruba_telemetry_proto.bleData.frameType)


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
