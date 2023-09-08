FROM node:18-buster

RUN apt update
RUN apt-get update \
    && apt-get install -y libsm6 libxext6 git ninja-build libglib2.0-0 libsm6 libxrender-dev libxext6 default-libmysqlclient-dev build-essential \
    && apt install -y zip screen libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /
RUN git clone https://github.com/romndev/autoannotator-ui.git /app
WORKDIR /app

ENV NODE_ENV dev

RUN yarn --frozen-lockfile
RUN yarn install
# RUN yarn run dev