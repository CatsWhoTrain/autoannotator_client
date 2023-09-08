FROM node:18-buster

RUN apt update
RUN apt-get update \
    && apt-get install -y git

WORKDIR /
RUN git clone https://github.com/romndev/autoannotator-ui.git /app
WORKDIR /app
ENV NODE_ENV dev

RUN yarn