#local host version
import random

max_attempt = 6

#words = ["apple", "grape", "sugar", "flame", "brave"]

def load_words(filename):
    with open(filename, "r") as file:
        words = [line.strip().lower() for line in file if len(line.strip()) == 5 and line.strip().isalpha()]
    # ensure the list contains only 5-letter words
    words = [word for word in words if len(word) == 5]
    return words

def get_feedback(guess, answer):
    feedback = []
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            feedback.append("🟩")  # Correct letter and position
        elif guess[i] in answer:
            feedback.append("🟨")  # Correct letter, wrong position
        else:
            feedback.append("⬜")  # Letter not in word
    # return "".join(feedback)
    return (feedback)

def is_valid(word,words):
    return len(word) == 5 and word.isalpha() and word in words

def play():
    words = load_words("5-letter_words.txt")
    answer = random.choice(words)
    print("🎯 Welcome to Wordle! Guess the 5-letter word.")
    attempts = 0
    #testing, remove later
    print(answer)

    while attempts < max_attempt:
        guess = input(f"Attempt {attempts + 1}/{max_attempt}: ").lower()
        if not is_valid(guess,words):
            print("❌ Invalid input. Please enter a 5-letter legal word.")
            continue

        feedback = get_feedback(guess, answer)
        print(f"Feedback: {feedback}")

        if guess == answer:
            print("You win!!")
            break

        attempts += 1

    else:
        print(f"💀 Game over! The word was: {answer}")

if __name__ == "__main__":
    play()
