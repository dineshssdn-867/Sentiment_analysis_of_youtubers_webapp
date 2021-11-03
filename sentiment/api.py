import requests
import json
from decouple import config

def analyze_emotion(text):
    url = "https://api.twinword.com/api/emotion/analyze/latest/"
    querystring = {"text":text}

    headers = {
    'Content-Type': "application/json",
    'Host': "api.twinword.com",
    'X-Twaip-Key': config('API_KEY'),
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)
    return response