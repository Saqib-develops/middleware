from langdetect import detect
from googletrans import Translator

translator = Translator()

def preprocess_user_message(user_text):
    """Detect language + translate to English for Rasa"""
    try:
        detected_lang = detect(user_text)
    except:
        detected_lang = "en"

    if detected_lang != "en":
        translated = translator.translate(user_text, src=detected_lang, dest="en").text
        return translated, detected_lang
    return user_text, "en"


def postprocess_bot_response(bot_text, target_lang):
    """Translate Rasa response (English) back to user's language"""
    if target_lang != "en":
        translated = translator.translate(bot_text, src="en", dest=target_lang).text
        return translated
    return bot_text
