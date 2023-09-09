FROM ubuntu:22.04
RUN apt update && apt install -y python3 python3-pip

RUN apt-get update \
    && apt-get install -y ffmpeg libsm6 libxext6 git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 python3.8-dev default-libmysqlclient-dev build-essential \
    && apt install -y zip htop screen libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip3 install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
COPY ./annotations.json /app/annotations.json
RUN pip3 install -r requirements.txt

RUN pip3 install autoannotator==0.0.6

COPY src /app/src
COPY test.py /app/test.py
COPY main.py /app/main.py
