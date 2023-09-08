FROM ubuntu:22.04

RUN apt update
RUN apt-get update \
    && apt-get install -y zip libsm6 libxext6 ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 default-libmysqlclient-dev build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN apt update && apt install -y python3 python3-pip

WORKDIR /app

RUN pip3 install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY main.py /app/main.py
