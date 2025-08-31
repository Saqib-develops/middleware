from langdetect import detect
from googletrans import Translator

import asyncio

translator = Translator()

async def preprocess_user_message(user_text):
    detected = translator.detect(user_text)
    detected_lang = detected.lang if detected else "en"

    # Await the coroutine
    translated = await translator.translate(user_text, src=detected_lang, dest="en")
    return translated.text, detected_lang


def postprocess_bot_response(bot_text, target_lang):
    """Translate Rasa response (English) back to user's language"""
    if target_lang != "en":
        translated = translator.translate(bot_text, src="en", dest=target_lang).text
        return translated
    return bot_text
