import logging

class ATC:
    def __init__(self, mac, name):
        self.mac = mac
        self.name = name
        self.rssi = 0

    def parse_payload(self, payload):
        local_name = None
        uuid = None
        self.temp = None
        self.humi = None
        self.battery = None

        if payload[0:3].hex() != '020106':
            logging.error("No BtHome Packet")
            return None

        payload_length = int.from_bytes(payload[3:4], "big", signed=False)

        payload_type = int.from_bytes(payload[4:5], "big", signed=False)
        # Complete local name
        if (payload_type == 9):
            local_name = payload[5:5 + payload_length].decode("utf-8", "ignore")

        # Service Data - 16-bit UUID
        if (payload_type == 22):
            uuid = payload[5:7].hex()

            if payload[7:8].hex() == '02':
                # 000 00010
                # Object length: 2
                # unsigned integer

                logging.debug("Got bthome packet: %s", payload);

                # packet id
                if payload[8:9].hex() == '00':
                    packet_id = int.from_bytes(payload[9:10], "big", signed=False)

                    # Object ID 0x23 - Temperature
                    if payload[10:11].hex() == '23':
                        # 001 00011
                        # Object length: 3
                        # 001 -> signed integer

                        # Temperature  	0.01
                        if payload[11:12].hex() == '02':
                            self.temp = int.from_bytes(payload[12:14], "little", signed=True) / 100

                    # Object ID 0x03 - humidity
                    if payload[14:15].hex() == '03':
                        # 000 00011
                        # Object length: 3
                        # 000 -> unsigned integer

                        # humidity 0.01
                        if payload[15:16].hex() == '03':
                            self.humi = int.from_bytes(payload[16:18], "little", signed=False) / 100

                    # Object ID 0x02 - ? (battery percentage in my tests so far...)
                    if payload[18:19].hex() == '02':
                        # 000 00010
                        # Object length: 2
                        # 000 -> unsigned integer

                        # battery 1 %
                        if payload[19:20].hex() == '01':
                            self.battery = int.from_bytes(payload[20:21], "little", signed=False)

        return {
            "payload_length": payload_length,
            "local_name": local_name,
            "payload_type": payload_type,
            "uuid": uuid,
            "packet_id": packet_id,
            "temp": self.temp,
            "humi": self.humi,
            "battery": self.battery
        }
