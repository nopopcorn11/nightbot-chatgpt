from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")  # Set API key in Koyeb environment variables

@app.route("/ask", methods=["GET"])
def ask():
    question = request.args.get("q", "")
    
    if not question:
        return jsonify({"response": "Please provide a question after !ask"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Answer concisely under 400 characters."},
                      {"role": "user", "content": question}],
            max_tokens=100
        )
        answer = response["choices"][0]["message"]["content"].strip()
        return jsonify({"response": answer[:400]})  # Ensure response is within Nightbot's limit

    except Exception as e:
        return jsonify({"response": "Error generating response"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
