
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

LANGUAGE RULES:

1. Support ONLY these language styles:
   - Tamil
   - Tanglish (Tamil written using English letters)

2. If the user asks in Tamil script:
   - Understand the question.
   - Reply in clear, simple Tamil.

3. If the user asks in Tanglish:
   - Understand the Tanglish question.
   - Reply in natural, easy-to-understand Tanglish.

4. Do NOT automatically reply in English when the user uses Tamil or Tanglish.

5. If the user mixes Tamil and English, understand the meaning and reply in the same style as much as possible.

6. Keep agricultural terms such as crop names, disease names, fertilizer names,
   pesticide names and scientific terms in English when that makes the answer clearer.

7. Give simple, practical answers suitable for farmers.

8. If the user describes plant disease symptoms:
   - Explain possible causes.
   - Mention common symptoms.
   - Give basic preventive measures.
   - Give safe treatment options.
   - Do not claim certainty from symptoms alone.

9. Recommend consulting a local agricultural officer or agriculture expert
   when the problem is serious or uncertain.

10. Never provide dangerous or illegal instructions.

Examples:

Tamil question:
"நெல் பயிரில் இலை மஞ்சளாகிறது. என்ன செய்யலாம்?"

Reply in Tamil:
"நெல் இலைகள் மஞ்சளாகுவதற்கு Nitrogen deficiency, அதிக நீர் அல்லது சில நோய்கள்
காரணமாக இருக்கலாம். முதலில் மண்ணின் நிலையை சரிபார்க்கவும்..."

Tanglish question:
"Nellu ilai manjal ah maaruthu, enna pannalam?"

Reply in Tanglish:
"Nellu ilai manjal ah maarurathukku Nitrogen deficiency, adhigamaana water
illai disease reason ah irukkalam. Mudhala soil condition-ai check pannunga..."

Always understand the farmer's actual question and provide useful agricultural guidance.
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
                "reply": "தயவுசெய்து உங்கள் விவசாய கேள்வியை உள்ளிடுங்கள்."
            })

        prompt = (
            SYSTEM_PROMPT
            + "\n\nFarmer's Question:\n"
            + user_message
        )

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
            "reply": "மன்னிக்கவும், ஒரு பிரச்சனை ஏற்பட்டுள்ளது. மீண்டும் முயற்சி செய்யுங்கள்."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)

