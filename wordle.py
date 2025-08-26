{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "7b12ffc1-2a68-40ff-ae78-e0b9265bda90",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "🎯 Welcome to Wordle! Guess the 5-letter word.\n",
      "deify\n"
     ]
    }
   ],
   "source": [
    "import random\n",
    "\n",
    "max_attempt = 6\n",
    "\n",
    "#words = [\"apple\", \"grape\", \"sugar\", \"flame\", \"brave\"]\n",
    "\n",
    "def load_words(filename):\n",
    "    with open(filename, \"r\") as file:\n",
    "        words = [line.strip().lower() for line in file if len(line.strip()) == 5 and line.strip().isalpha()]\n",
    "    # ensure the list contains only 5-letter words\n",
    "    words = [word for word in words if len(word) == 5]\n",
    "    return words\n",
    "\n",
    "def get_feedback(guess, answer):\n",
    "    feedback = []\n",
    "    for i in range(len(guess)):\n",
    "        if guess[i] == answer[i]:\n",
    "            feedback.append(\"🟩\")  # Correct letter and position\n",
    "        elif guess[i] in answer:\n",
    "            feedback.append(\"🟨\")  # Correct letter, wrong position\n",
    "        else:\n",
    "            feedback.append(\"⬜\")  # Letter not in word\n",
    "    # return \"\".join(feedback)\n",
    "    return (feedback)\n",
    "\n",
    "def is_valid(word):\n",
    "    #ToDo - word validation\n",
    "    return len(word) == 5 and word.isalpha()\n",
    "\n",
    "def play():\n",
    "    words = load_words(\"5-letter_words.txt\")\n",
    "    answer = random.choice(words)\n",
    "    print(\"🎯 Welcome to Wordle! Guess the 5-letter word.\")\n",
    "    attempts = 0\n",
    "    #testing, remove later\n",
    "    print(answer)\n",
    "\n",
    "    while attempts < max_attempt:\n",
    "        guess = input(f\"Attempt {attempts + 1}/{max_attempt}: \").lower()\n",
    "        if not is_valid(guess):\n",
    "            print(\"❌ Invalid input. Please enter a 5-letter word.\")\n",
    "            continue\n",
    "\n",
    "        feedback = get_feedback(guess, answer)\n",
    "        print(f\"Feedback: {feedback}\")\n",
    "\n",
    "        if guess == answer:\n",
    "            print(\"You win!!\")\n",
    "            break\n",
    "\n",
    "        attempts += 1\n",
    "\n",
    "    else:\n",
    "        print(f\"💀 Game over! The word was: {answer}\")\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    play()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "id": "8031cc4d-266e-44cc-8835-c98708886321",
   "metadata": {},
   "outputs": [
    {
     "ename": "SyntaxError",
     "evalue": "invalid syntax (1977679806.py, line 9)",
     "output_type": "error",
     "traceback": [
      "\u001b[1;36m  Cell \u001b[1;32mIn[22], line 9\u001b[1;36m\u001b[0m\n\u001b[1;33m    for i in words if len(i) == 5:\u001b[0m\n\u001b[1;37m                                 ^\u001b[0m\n\u001b[1;31mSyntaxError\u001b[0m\u001b[1;31m:\u001b[0m invalid syntax\n"
     ]
    }
   ],
   "source": [
    "\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "b2883a24-f54f-47e5-bef7-346c00063a92",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
