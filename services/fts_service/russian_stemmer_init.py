import requests
import json
headers = {
        'Content-Type': 'application/json'
    }
req = requests.put('http://localhost:9200/rebuilt_russian', headers=headers, data=json.dumps(
    {
        "settings": {
            "analysis": {
                "filter": {
                    "russian_stop": {
                        "type": "stop",
                        "stopwords": "_russian_"
                    },
                    "russian_stemmer": {
                        "type": "stemmer",
                        "language": "russian"
                    }
                },
                "analyzer": {
                    "rebuilt_russian": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "decimal_digit",
                            "russian_stop",
                            # "russian_normalization",
                            #"russian_keywords",
                            "russian_stemmer"
                        ]
                    }
                }
            }
        }
    }))

print(req.text)
