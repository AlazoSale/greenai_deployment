import requests
from api.misc.constants import SUPPORTED_LANGUAGES
from os import environ


def translate_text(text, target_language, source_language):
    headers = {
        'Ocp-Apim-Subscription-Key': environ.get('subscription_key'),
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Region': environ.get('region'),
    }    
    params = {
        'to': SUPPORTED_LANGUAGES[target_language],
    }    
    if source_language:
        params['from'] = SUPPORTED_LANGUAGES[source_language]    
    response = requests.post(environ.get('translation_endpoint'), headers=headers, params=params, json=[{'Text': text}])
    response.raise_for_status()
    
    translation = response.json()[0]['translations'][0]['text']
    print("Translated text:", translation)
    return translation
