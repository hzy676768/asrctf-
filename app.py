import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.json

        headers = {
            "Content-Type": "application/json"
        }

        # Only attach Authorization header if API key exists
        if OLLAMA_API_KEY:
            headers["Authorization"] = f"Bearer {OLLAMA_API_KEY}"

        # Ollama Cloud endpoint
        if "api.ollama.com" in OLLAMA_BASE_URL:
            url = f"{OLLAMA_BASE_URL}/v1/chat/completions"
        else:
            # Local Ollama endpoint
            url = f"{OLLAMA_BASE_URL}/api/chat"

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=60
        )

        return jsonify(response.json())

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
