import os
import json
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

with open("thirukkural_data.json", "r", encoding="utf-8") as f:
    thirukkural = json.load(f)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "").strip().lower()

    if message.isdigit():
        num = int(message)
        if 1 <= num <= 1330:
            kural = thirukkural.get(str(num), {})
            return jsonify({
                "response": kural,
                "source": "local"
            })

    try:
        prompt = f"Answer this in Tamil and English based on Thirukkural: {message}"
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        answer = res.choices[0].message.content.strip()
        return jsonify({"response": {"message": answer}, "source": "openai"})
    except Exception as e:
        return jsonify({"response": {"message": "Sorry, an error occurred."}, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
