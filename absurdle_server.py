# absurdle_server.py
from flask import Flask, request, jsonify
import random

app = Flask(__name__)
word_list = [line.strip().lower() for line in open("5-letter_words.txt") if len(line.strip()) == 5]
# Starts with all valid words as possible answers
possible_answers = set(word_list)  

def get_feedback(guess, answer):
    feedback = []
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            feedback.append("green")
        elif guess[i] in answer:
            feedback.append("yellow")
        else:
            feedback.append("gray")
    return tuple(feedback)  # Use tuple for hashing

@app.route("/guess", methods=["POST"])
def guess():
    global possible_answers

    data = request.json
    guess_word = data.get("word", "").lower()

    if guess_word not in word_list:
        return jsonify({"error": "Invalid word"}), 400

    # Partition possible answers by feedback pattern
    partitions = {}
    for word in possible_answers:
        fb = get_feedback(guess_word, word)
        partitions.setdefault(fb, set()).add(word)

    # Choose the largest partition (least helpful)
    worst_feedback = max(partitions.items(), key=lambda x: len(x[1]))
    feedback, new_possible_answers = worst_feedback
    possible_answers = new_possible_answers

    # If only one word remains and guess matches it, player wins
    win = len(possible_answers) == 1 and guess_word in possible_answers

    return jsonify({
        "feedback": list(feedback),
        "win": win
    })

@app.route("/reset", methods=["POST"])
def reset():
    global possible_answers
    possible_answers = set(word_list)
    return jsonify({"status": "reset"})

if __name__ == "__main__":
    app.run(port=5000)