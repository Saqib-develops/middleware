from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS 
import asyncio
from translator_middleware import preprocess_user_message, postprocess_bot_response


app = Flask(__name__)
CORS(app)

# Rasa backend URL
RASA_URL  = "https://language-agnostic-chatbot.onrender.com/webhooks/rest/webhook"


@app.route("/chat", methods=["POST"])
async def chat():
    data = request.json
    user_msg = data.get("message", "")

    translated_msg, lang = await preprocess_user_message(user_msg)

    # forward to Rasa or your logic...
    response = {"reply": f"Processed: {translated_msg} (lang: {lang})"}
    return jsonify(response)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
