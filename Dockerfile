# syntax=docker/dockerfile:1

FROM ubuntu:22.04

RUN apt update && apt install -y python3-dev python3-pip unzip

COPY requirements.txt *.py /
COPY aos8-iot-server-example-websocket /aos8-iot-server-example-websocket

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


ADD https://github.com/protocolbuffers/protobuf/releases/download/v25.1/protoc-25.1-linux-x86_64.zip protoc.zip
RUN unzip protoc.zip
RUN mv bin/protoc /usr/local/bin/protoc

RUN /usr/local/bin/protoc -I=./aos8-iot-server-example-websocket/proto_files/source/ --python_out=. --pyi_out=./ ./aos8-iot-server-example-websocket/proto_files/source/aruba-iot-*

ENTRYPOINT [ "python3", "main.py" ]
