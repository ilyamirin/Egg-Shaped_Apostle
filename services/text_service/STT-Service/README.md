# STT Service

The service is intended for speech recognition in an audio file using DeepSpeech model or other model

## Prerequisites
* Git LFS (ensure you ran 'git lfs pull')
* Docker

## Run
Build docker image and run container via commands:
```bash
docker build -t apostle-stt-service .
docker run -p ${APP_PORT}:5000 -d --rm --name apostle-stt-service apostle-stt-service
```

## Local Install for Development
Install virtual eviroment and python requirements via commands:
```bash
virtualenv --system-site-packages -p python3 ./.venv
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install --upgrade -r requirements.txt
```

# API

Description of the provided routes

## Health

Route to check the service is alive

> GET /health

Response:
```json
{
    "service": "stt-service",
    "status": "OK"
}
```

## Transcribe

Main route for transcribing an audio file

> POST /transcribe

Request:
 * Content-Type: multipart/form-data
 * Field 'audio' with file

Successful response: (200 OK)
```json
{
    "result": "experience proves this"
}
```

Error response: (400 BAD REQUEST / 500 INTERNAL ERROR)
```json
{
    "message": "No file provided",
    "type": "BadRequestException"
}
```
