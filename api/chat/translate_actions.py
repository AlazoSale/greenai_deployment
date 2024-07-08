import requests
from django.conf import settings
from api.misc import constants as miscConstants
import os, time, threading
from os import environ
import azure.cognitiveservices.speech as speechsdk

#http://localhost:8000/api/translate/?text_to_translate=YourTextHere&target_lang=Hindi&source_lang=English
def T2T_translation(text, target_language, source_language):
    headers = {
        'Ocp-Apim-Subscription-Key': settings.T2T_SUBSCRIPTION_KEY,
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Region': settings.T2T_REGION
    }    
    params = {
        'to': miscConstants.SUPPORTED_T2T_LANGUAGES[target_language],
    }    
    if source_language:
        params['from'] = miscConstants.SUPPORTED_T2T_LANGUAGES[source_language]    
    response = requests.post(settings.T2T_TRANSLATION_ENDPOINT, headers=headers, params=params, json=[{'Text': text}])
    response.raise_for_status()
    
    translation = response.json()[0]['translations'][0]['text']
    print("Translated text:", translation)
    return translation



"""
#http://localhost:8000/api/chat/translate/STT/?target_lang=TEnglish&source_lang=SEnglish
def STT_translation(target_language, source_language, s_aud):
        Function to continuously read and translate audio with timeout of 10s.
        Calls another function to process audio chunk.
        Can set target and source language in params, expects file called s_aud
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=environ.get('STT_subscription_key'),
                                                                          region=environ.get('STT_region'))

    speech_translation_config.speech_recognition_language=miscConstants.SUPPORTED_STT_LANGUAGES[source_language]

    target_language=miscConstants.SUPPORTED_STT_LANGUAGES[target_language]
    speech_translation_config.add_target_language(target_language)
 
    p_aud = handle_uploaded_audio(s_aud)
    audio_config = speechsdk.audio.AudioConfig(filename=p_aud)
    translation_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=speech_translation_config, audio_config=audio_config)
    recognized_text = []
    # function to handle recognition event

    def handle_result(evt):
        recognized_text.append(evt.result.text)

    translation_recognizer.recognized.connect(handle_result)

    done_event = threading.Event() 

    # Callback function for recognizing events
    def recognition_completed(evt):
        done_event.set()

    translation_recognizer.session_stopped.connect(recognition_completed)
    translation_recognizer.canceled.connect(recognition_completed)
    translation_recognizer.start_continuous_recognition()

    done_event.wait() #remove timeout for entire file recognition

    translation_recognizer.stop_continuous_recognition()

    return recognized_text
"""

def STT_translation(target_language, source_language, s_aud):
    print(f"The s_aud file: {s_aud}")
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=settings.STT_SUBSCRIPTION,
                                                                          region= settings.STT_REGION)

    speech_translation_config.speech_recognition_language=miscConstants.SUPPORTED_STT_LANGUAGES[source_language]

    target_language=miscConstants.SUPPORTED_STT_LANGUAGES[target_language]
    speech_translation_config.add_target_language(target_language)

    p_aud = handle_uploaded_audio(s_aud)

    audio_config = speechsdk.audio.AudioConfig(filename=p_aud)
    translation_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=speech_translation_config, audio_config=audio_config)
  
    translation_recognition_result = translation_recognizer.recognize_once()
    if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
       return translation_recognition_result.translations[target_language]
    elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        return ("No speech could be recognized: {}".format(translation_recognition_result.no_match_details))
    elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = translation_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")


def handle_uploaded_audio(uploaded_audio_file):
  """
  Function to process the audio
  """
  filename = uploaded_audio_file.name

  with open(filename, 'wb') as f:
    for chunk in uploaded_audio_file.chunks():
      f.write(chunk)
  return filename



