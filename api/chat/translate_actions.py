import requests
from api.misc.constants import SUPPORTED_LANGUAGES
from django.conf import settings


def translate_text(text, target_language, source_language):
    headers = {
        'Ocp-Apim-Subscription-Key': settings.SUBSCRIPTION_KEY,
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Region': settings.REGION,
    }    
    params = {
        'to': SUPPORTED_LANGUAGES[target_language],
    }    
    if source_language:
        params['from'] = SUPPORTED_LANGUAGES[source_language]    
    response = requests.post(settings.TRANSLATION_ENDPOINT, headers=headers, params=params, json=[{'Text': text}])
    response.raise_for_status()
    
    translation = response.json()[0]['translations'][0]['text']
    print("Translated text:", translation)
    return translation
