import requests
import json
from decouple import config


def analyze_emotion(text):
    url = config('API')
    querystring = {"text": text}
    response = requests.post(url, data=querystring)
    response = json.loads(response.text)
    return response
