from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS 
from translator_middleware import preprocess_user_message, postprocess_bot_response


app = Flask(__name__)
CORS(app)

# Rasa backend URL
RASA_URL  = "https://language-agnostic-chatbot.onrender.com/webhooks/rest/webhook"


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    # Step 1: Preprocess user text (detect + translate to English)
    translated_msg, lang = preprocess_user_message(user_msg)

    # Step 2: Send to Rasa
    rasa_response = requests.post(RASA_URL, json={"sender": "user", "message": translated_msg})
    rasa_response = rasa_response.json()

    # Step 3: Translate Rasa response back to user’s language
    final_responses = []
    for res in rasa_response:
        bot_text = res.get("text")
        if bot_text:
            translated_text = postprocess_bot_response(bot_text, lang)
            final_responses.append({"text": translated_text})

    return jsonify(final_responses)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
