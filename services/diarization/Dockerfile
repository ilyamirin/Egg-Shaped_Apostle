FROM nvidia/cuda:10.2-cudnn7-devel

RUN apt-get update && apt-get install -y python3-pip git
RUN pip3 install -U virtualenv

WORKDIR /app

COPY requirements.txt ./
RUN virtualenv --system-site-packages -p python3 ./.venv
RUN ./.venv/bin/pip install --upgrade pip
RUN ./.venv/bin/pip install --upgrade -r requirements.txt
RUN git clone https://github.com/pyannote/pyannote-audio.git
WORKDIR pyannote-audio
RUN .././.venv/bin/pip install .
COPY resources resources
COPY src src

EXPOSE 5000

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

ENTRYPOINT .venv/bin/python3.6 src/web.py
