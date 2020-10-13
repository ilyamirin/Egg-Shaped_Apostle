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
####GET /annotation
Curl:
```
curl -H "Filename: 0_0_0_2020-10-14T01:10:19.010726.wav" -X GET 127.0.0.1:5732/annotation
```
####GET /svg
Make sure that you are trying to get svg AFTER you used GET /annotation on file 
Curl:
```
curl -H "filename: 0_3_0_2020-09-08T04:16:14.336006.wav" http://127.0.0.1:5732/svg
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
