# aruba2mqtt

## Installation

Create protbuf files
- Download [protoc](https://github.com/protocolbuffers/protobuf/releases)

``` text
git submodule update --init --recursive

./protoc -I=./aos8-iot-server-example-websocket/proto_files/source/ --python_out=. --pyi_out=./ ./aos8-iot-server-example-websocket/proto_files/source/aruba-iot-* 

pip3 install -r requirements.txt
```

### Demo
![img.png](img.png)