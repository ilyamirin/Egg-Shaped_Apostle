# Diarization module
## Usage:
###Web API:
####GET /health
Returns json object
```
{
        'service': 'diarization-service',
        'status': 'OK'
    }
```
####POST /diarizate
should be file named "audio"
Curl:
```
curl -F "audio=@test.wav" 127.0.0.1:5732/diarizate
```
## Deploy:
###Docker
####TBD
###On the host machine (Ubuntu 18.04 as OS):
1) Make sure you have Nvidia Cuda 10.2 installed.
2) Update apt, install pip
```
apt-get update && apt-get install -y python3-pip
```
3) Install venv:
```
pip3 install -U virtualenv
```
4) In Egg-Shaped_Apostle/services/diarization as current directory,
```
python3 -m venv ./venv
```
5) Activate environment:
```
source ./.venv/bin/activate
```
6) install requirements:
```
pip install -r requirements.txt
```
7) install pyannote:
```
git clone https://github.com/pyannote/pyannote-audio.git
cd pyannote-audio
git checkout develop
pip install .
```