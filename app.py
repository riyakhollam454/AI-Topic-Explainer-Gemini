from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os


# --------------------------------------------------
# Load environment variables from .env
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Get Gemini API Key
# --------------------------------------------------

api_key = os.getenv("GEMINI_API_KEY")


# --------------------------------------------------
# Check whether API key exists
# --------------------------------------------------

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. "
        "Please add your Gemini API key to the .env file."
    )


# --------------------------------------------------
# Create Flask application
# --------------------------------------------------

app = Flask(__name__)


# --------------------------------------------------
# Create Gemini client
# --------------------------------------------------

client = genai.Client(
    api_key="API_KEY"
)


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# Chat API
# --------------------------------------------------

@app.route("/chat", methods=["POST"])
def chat():

    try:

        # Get JSON data from frontend
        data = request.get_json()

        # Get user's message
        user_message = data.get("message", "").strip()

        # Check empty message
        if not user_message:
            return jsonify({
                "error": "Please enter a message."
            }), 400


        # --------------------------------------------------
        # Send message to Gemini
        # --------------------------------------------------

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )


        # Get Gemini response
        answer = response.text


        # Send response back to JavaScript
        return jsonify({
            "response": answer
        })


    except Exception as e:

        print("Gemini Error:", e)

        return jsonify({
            "error": str(e)
        }), 500


# --------------------------------------------------
# Run Flask application
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
