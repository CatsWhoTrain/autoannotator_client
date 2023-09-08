FROM ubuntu:22.04

RUN mkdir /app

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

# COPY . /app
