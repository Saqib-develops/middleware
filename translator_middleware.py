from langdetect import detect
from googletrans import Translator

import asyncio

translator = Translator()

def preprocess_user_message(user_text: str):
    detected = translator.detect(user_text)
    detected_lang = detected.lang if detected else "en"
    translated = translator.translate(user_text, src=detected_lang, dest="en")
    return translated.text, detected_lang

def postprocess_bot_response(bot_text: str, target_lang: str):
    if target_lang == "en":
        return bot_text
    translated = translator.translate(bot_text, src="en", dest=target_lang)
    return translated.text
