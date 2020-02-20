import requests
import json
import yaml

with open('api-key.yaml') as file:
    api_key = yaml.load(file, Loader=yaml.FullLoader)['secret']

#with open("auido_file.wav", "rb") as f:
#    data = f.read()

auth = {"Authorization": "Api-Key " + api_key}
resource = r'https://stt.api.cloud.yandex.net:443'

params = {
        "config": {
            "specification": {
                "languageCode": "ru-RU",
                "model": "general:rc",
                "profanityFilter": "true",
                "partialResults": "false",
                "singleUtterance": "false",
                "audioEncoding": "LINEAR16_PCM",
                "sampleRateHertz": "48000",
                "rawResults": "false",
                "audioChannelCount": "1"
            }
        }
    }

payload = json.dumps(params)
response = requests.post(resource, data=payload, headers=auth).request
print(response)
#"audio_content": {
#    "uri": obj_link
#}