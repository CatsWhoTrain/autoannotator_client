FROM ubuntu:22.04
RUN apt update && apt install -y python3 python3-pip

WORKDIR /app

RUN pip3 install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
COPY ./annotations.json /app/annotations.json
RUN pip3 install -r requirements.txt

COPY main.py /app/main.py
