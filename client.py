# Server/Client version with ui
# client.py
import tkinter as tk
import random
import requests

max_attempts = 6
word_length = 5
word_file = "5-letter_words.txt"

def load_words(filename):
    with open(filename, "r") as file:
        words = [line.strip().lower() for line in file if len(line.strip()) == word_length and line.strip().isalpha()]
    return words

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

def is_valid(word, word_list):
    return len(word) == word_length and word in word_list

class WordleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle Game")
        self.words = load_words(word_file)
        self.answer = random.choice(self.words)
        self.attempts = 0
        self.current_guess = ""
        self.guess_labels = []
        self.keyboard_buttons = {}
        self.message_label = None

        self.create_ui()
        self.root.bind("<Key>", self.handle_keypress)
        # Remove later
        print(f"test answer: {self.answer}")

    # Config the UI layout
    def create_ui(self):
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=10)

        for row in range(max_attempts):
            row_labels = []
            for col in range(word_length):
                lbl = tk.Label(self.grid_frame, text=" ", width=4, height=2, font=("Helvetica", 18), relief="solid", bg="white")
                lbl.grid(row=row, column=col, padx=2, pady=2)
                row_labels.append(lbl)
            self.guess_labels.append(row_labels)

        self.keyboard_frame = tk.Frame(self.root)
        self.keyboard_frame.pack()

        keys_row1 = "QWERTYUIOP"
        keys_row2 = "ASDFGHJKL"
        keys_row3 = "ZXCVBNM"
        
        # Row 1
        for i, letter in enumerate(keys_row1):
            btn = tk.Button(self.keyboard_frame, text=letter, width=4, height=2, command=lambda l=letter: self.add_letter(l))
            btn.grid(row=0, column=i, padx=2, pady=2)
            self.keyboard_buttons[letter.lower()] = btn
        
        # Row 2
        for i, letter in enumerate(keys_row2):
            btn = tk.Button(self.keyboard_frame, text=letter, width=4, height=2, command=lambda l=letter: self.add_letter(l))
            btn.grid(row=1, column=i + 1, padx=2, pady=2)  # Indented for alignment
            self.keyboard_buttons[letter.lower()] = btn
        
        # Row 3
        for i, letter in enumerate(keys_row3):
            btn = tk.Button(self.keyboard_frame, text=letter, width=4, height=2, command=lambda l=letter: self.add_letter(l))
            btn.grid(row=2, column=i + 1, padx=2, pady=2)  # Further indented for alignment
            self.keyboard_buttons[letter.lower()] = btn
    
    
        # Add backspace and submit buttons
        self.backspace_btn = tk.Button(self.keyboard_frame, text="←", width=4, height=2, command=self.backspace)
        self.backspace_btn.grid(row=3, column=7, padx=2, pady=2)
        
        self.enter_btn = tk.Button(self.keyboard_frame, text="Enter", width=6, height=2, command=self.submit_guess)
        self.enter_btn.grid(row=3, column=8, columnspan=2, padx=2, pady=2)
        """
        btn= tk.Button(self.keyboard_frame, text="←", width=4, height=2, command=self.backspace)
        btn.grid(row=3, column=7, padx=2, pady=2)
        self.keyboard_buttons[letter.lower()] = btn
        btn=tk.Button(self.keyboard_frame, text="Enter", width=6, height=2, command=self.submit_guess)
        btn.grid(row=3, column=8, columnspan=2, padx=2, pady=2)
        #self.keyboard_buttons[letter.lower()] = btn
        """
        self.message_label = tk.Label(self.root, text="", font=("Helvetica", 14), fg="red")
        self.message_label.pack(pady=5)

        
    # Add letter to the grid
    def add_letter(self, letter):
        if len(self.current_guess) < word_length:
            self.current_guess += letter.lower()
            self.update_grid()

    def backspace(self):
        self.current_guess = self.current_guess[:-1]
        self.update_grid()

    def update_grid(self):
        row = self.attempts
        for i in range(word_length):
            char = self.current_guess[i].upper() if i < len(self.current_guess) else " "
            self.guess_labels[row][i].config(text=char)

    def submit_guess(self):
        if len(self.current_guess) != word_length:
            self.show_message("Not enough letters")
            return
    
        try:
            response = requests.post("http://localhost:5000/guess", json={"word": self.current_guess})
            data = response.json()
        except Exception as e:
            self.show_message("Server error")
            return
    
        if "error" in data:
            #self.show_message(data["                                                      "])
            self.show_message(data)
            return
    
        feedback = data["feedback"]
        for i, color in enumerate(feedback):
            self.guess_labels[self.attempts][i].config(bg=color)
            self.update_keyboard_color(self.current_guess[i], color)
    
        if data["win"]:
            self.show_message("🎉 You win!", success=True)
            self.root.unbind("<Key>")
            for btn in self.keyboard_buttons.values():
                btn.config(state="disabled")
            self.backspace_btn.config(state="disabled")
            self.enter_btn.config(state="disabled")
            return
    
        self.attempts += 1
        self.current_guess = ""
    
        if self.attempts == max_attempts:
            self.show_message("💀 Game over!")
            self.root.unbind("<Key>")
            for btn in self.keyboard_buttons.values():
                btn.config(state="disabled")
            self.backspace_btn.config(state="disabled")
            self.enter_btn.config(state="disabled")


    def update_keyboard_color(self, letter, color):
        btn = self.keyboard_buttons.get(letter)
        if btn:
            current = btn.cget("bg")
            # Prioritize showing color green > yellow > gray
            if current == "green":
                return
            elif current == "yellow" and color == "gray":
                return
            btn.config(bg=color)

    def show_message(self, msg, success=False):
        self.message_label.config(text=msg, fg="green" if success else "red")
        if not success:
            self.root.after(2000, lambda: self.message_label.config(text=""))

    def handle_keypress(self, event):
        key = event.keysym.lower()
        if key == "backspace":
            self.backspace()
        elif key == "return":
            self.submit_guess()
        elif key.isalpha() and len(key) == 1:
            self.add_letter(key)



if __name__ == "__main__":
    root = tk.Tk()
    game = WordleGame(root)
    root.mainloop()