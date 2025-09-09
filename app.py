from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)

# Replace this locally with your real OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"

# Optional: Use environment variable (safer)
# openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type something!"})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful, friendly, and concise assistant."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=400,
            temperature=0.7
        )
        reply = response["choices"][0]["message"]["content"].strip()
    except openai.error.AuthenticationError:
        reply = "⚠️ API key is invalid. Please check your key."
    except openai.error.RateLimitError:
        reply = "⚠️ API quota exceeded. Please check your plan."
    except Exception as e:
        reply = f"⚠️ Error: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
