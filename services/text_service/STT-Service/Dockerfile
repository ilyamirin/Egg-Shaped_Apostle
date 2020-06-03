FROM ubuntu:18.04

RUN apt-get update

RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install -U virtualenv

WORKDIR /app

COPY requirements.txt ./
RUN virtualenv --system-site-packages -p python3 ./.venv
RUN ./.venv/bin/pip install --upgrade pip
RUN ./.venv/bin/pip install --upgrade -r requirements.txt

COPY src src
COPY resources resources

EXPOSE 5000

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

ENTRYPOINT .venv/bin/python3.6 src/web.py
