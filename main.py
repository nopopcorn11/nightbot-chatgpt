from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/ask", methods=["GET"])
def ask():
    question = request.args.get("q", "").strip()
    
    if not question:
        return jsonify({"response": "Please provide a question after !ask"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Provide a response under 400 characters."},
                {"role": "user", "content": question}
            ],
            max_tokens=100
        )
        answer = response["choices"][0]["message"]["content"].strip()
        
        return jsonify({"response": answer[:400]})  # Ensure response is under 400 characters

    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {e}")  # Log OpenAI errors
        return jsonify({"response": "Error generating response"}), 500

    except Exception as e:
        print(f"General Error: {e}")  # Log any other errors
        return jsonify({"response": "An error occurred"}), 500

# Ensure the correct port for Koyeb
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 for Koyeb
    app.run(host="0.0.0.0", port=port)
