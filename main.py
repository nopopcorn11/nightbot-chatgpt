from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/ask", methods=["GET"])
def ask():
    question = request.args.get("q", "").strip()

    if not question:
        return "Please provide a question after !ask", 400

    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Changed to gpt-4
            messages=[
                {"role": "system", "content": "Respond concisely and directly with only the answer."},
                {"role": "user", "content": question}
            ],
            max_tokens=100
        )
        answer = response.choices[0].message.content.strip()

        # Ensure response is under 400 characters
        return answer[:400]

    except openai.OpenAIError as e:
        if "insufficient_quota" in str(e):
            return "Error: API quota exceeded. Try again later or check OpenAI billing.", 500
        print(f"OpenAI API Error: {e}")
        return "Error generating response", 500

    except Exception as e:
        print(f"General Error: {e}")
        return "An error occurred", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
