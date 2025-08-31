# Server/Client version with ui
# server.py

from flask import Flask, request, jsonify
import random

app = Flask(__name__)
words = [line.strip().lower() for line in open("5-letter_words.txt") if len(line.strip()) == 5]
answer = random.choice(words)
print(answer)

def get_feedback(guess, answer):
    feedback = []
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            feedback.append("green")
        elif guess[i] in answer:
            feedback.append("yellow")
        else:
            feedback.append("gray")
    return feedback

@app.route("/guess", methods=["POST"])
def guess():
    data = request.json
    guess_word = data.get("word", "").lower()
    if guess_word not in words:
        return jsonify({"error": "Invalid word"}), 400
    feedback = get_feedback(guess_word, answer)
    win = guess_word == answer
    return jsonify({"feedback": feedback, "win": win})

if __name__ == "__main__":
    app.run(port=5000)