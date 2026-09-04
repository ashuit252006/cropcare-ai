import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing in .env file")

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are CropCare AI, a friendly agricultural assistant.

Your job is to help farmers and agriculture students with:
- Crop diseases
- Plant symptoms
- Pest management
- Organic farming
- Irrigation
- Fertilizers
- Soil health
- Crop nutrition
- Weather-related crop care
- General farming guidance

Give simple, practical answers.
If the user describes plant disease symptoms, explain possible causes,
basic preventive measures and safe treatment options.

Do not claim certainty when diagnosing a disease from symptoms alone.
Recommend consulting a local agricultural expert when the problem is serious.

Answer in the same language/style used by the user.
"""

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "reply": "Please enter your farming question."
            })

        prompt = SYSTEM_PROMPT + "\n\nFarmer's Question:\n" + user_message

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        answer = response.text

        return jsonify({
            "reply": answer
        })

    except Exception as e:
        print("ERROR:", e)

        return jsonify({
            "reply": "Sorry, something went wrong. Please try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
