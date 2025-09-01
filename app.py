from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS
from translator_middleware import preprocess_user_message, postprocess_bot_response

app = Flask(__name__)
CORS(app)

# CORRECT URL for Render deployment
# This is the public address of your other Render service.
RASA_URL = "https://language-agnostic-chatbot.onrender.com/webhooks/rest/webhook"


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")

    try:
        translated_msg, lang = preprocess_user_message(user_msg)

        # Make the request to the Rasa server
        response = requests.post(
            RASA_URL,
            json={"sender": "user", "message": translated_msg},
            timeout=10  # Good practice: add a timeout
        )

        # Check for HTTP errors (like 4xx or 5xx responses)
        response.raise_for_status()

        # Try to parse the JSON response
        rasa_response = response.json()
        
        # If the response is empty (but valid JSON '[]'), handle it gracefully
        if not rasa_response:
            return jsonify([{"text": "I'm sorry, I don't have a response for that."}])

        # Process the response
        final_responses = []
        for res in rasa_response:
            bot_text = res.get("text")
            if bot_text:
                translated_text = postprocess_bot_response(bot_text, lang)
                final_responses.append({"text": translated_text})

        return jsonify(final_responses)

    # --- Error Handling Blocks ---
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error calling Rasa: {errh}")
        print(f"Rasa server response: {response.text}")
        return jsonify({"error": "There was an issue with the chatbot service."}), 502

    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON from Rasa.")
        print(f"Rasa server response: {response.text}")
        return jsonify({"error": "Received an invalid response from the chatbot service."}), 502

    except requests.exceptions.RequestException as err:
        print(f"Request Error calling Rasa: {err}")
        return jsonify({"error": "Could not connect to the chatbot service."}), 504

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
