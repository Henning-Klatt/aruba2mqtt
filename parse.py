import logging
def parse_payload(mac, rssi, payload):
    value_type = int.from_bytes(payload[0:1], "big", signed=False)
    temp = int.from_bytes(payload[21:23], "big", signed=True) / 10.0
    humidity = int.from_bytes(payload[9:10], "big")
    battery = int.from_bytes(payload[9:10], "big")
    battery_volts = int.from_bytes(payload[10:12], "big") / 1000.0
    counter = int.from_bytes(payload[12:13], "big")
    local_name = None
    uuid = None
    temp = None
    humi = None

    if payload[0:3].hex() != '020106':
        logging.error("No BtHome Packet")
        return None

    payload_length = int.from_bytes(payload[3:4], "big", signed=False)

    payload_type = int.from_bytes(payload[4:5], "big", signed=False)
    # Complete local name
    if(payload_type == 9):
        local_name = payload[5:5+payload_length].decode("utf-8", "ignore")

    # Service Data - 16-bit UUID
    if(payload_type == 22):
        uuid = payload[5:7].hex()

        if payload[7:8].hex() == '02':
            # 000 00010
            # Object length: 2
            # unsigned integer

            # packet id
            if payload[8:9].hex() == '00':
                packet_id = int.from_bytes(payload[9:10], "big", signed=False)

                # 0x23
                if payload[10:11].hex() == '23':
                    # 001 00011
                    # Object length: 3
                    # signed integer

                    # Temperature  	0.01
                    if payload[11:12].hex() == '02':
                        temp = int.from_bytes(payload[12:14], "little", signed=True) / 100
                # 0x03
                if payload[14:15].hex() == '03':
                    # 000 00011
                    # Object length: 3
                    # unsigned integer

                    # humidity 0.01
                    if payload[15:16].hex() == '03':
                        humi = int.from_bytes(payload[16:18], "little", signed=False) / 100

    return {
        "payload_length": payload_length,
        "local_name": local_name,
        "payload_type": payload_type,
        "uuid": uuid,
        "packet_id": packet_id,
        "temp" : temp,
        "humi" : humi
    }

#data_string = "020106 11 16 1c18 02 00 ee 23 02 05 08 03 03 94 1a 02 01 48"
#data_string = "0b094154435f453132314134"
#data_string = "0201060d161c1802006c021000030c7a0a"
#data_string = "02010611161c1802006d230200080303651a020144"
#data_string = "0b094154435f453132314134"
#data_string = "AgEGERYcGAIAjCMCbwcDAwAbAgE/"

#packet = bytes(bytearray.fromhex(data_string))
#packet = bytes(bytearray)


#result = parse_payload("", -94, packet)
#print(result)