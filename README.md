# aruba2mqtt

## Installation

Create protbuf files
- Download [protoc](https://github.com/protocolbuffers/protobuf/releases)

``` text
git submodule update
./protoc -I=./aos8-iot-server-example-websocket/proto_files/source/ --python_out=. --pyi_out=./ ./source/aruba-iot-* 
```


``` text
pip3 install -r requirements.txt
```