import tkinter as tk
from tkinter import ttk, messagebox
import random

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Number Guessing Game")
        self.root.geometry("430x470")
        self.root.resizable(False, False)

        self.difficulty = tk.StringVar(value="Medium")
        self.target_number = 0
        self.range_min = 1
        self.range_max = 100
        self.attempts = 0
        self.max_attempts = 10
        self.current_turn = "Player"
        self.player_score = 0
        self.ai_score = 0
        self.ai_guess_low = 0
        self.ai_guess_high = 0

        self.build_ui()

    def build_ui(self):
        ttk.Label(self.root, text="🎮 Number Guessing Game", font=("Arial", 16, "bold")).pack(pady=10)

        ttk.Label(self.root, text="Select Difficulty:").pack()
        ttk.Combobox(self.root, values=["Easy", "Medium", "Hard"], textvariable=self.difficulty,
                     state="readonly").pack(pady=5)

        self.start_button = ttk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

        self.status_label = ttk.Label(self.root, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.entry = ttk.Entry(self.root, font=("Arial", 12), justify="center")
        self.entry.pack(pady=5)
        self.entry.config(state="disabled")

        self.guess_button = ttk.Button(self.root, text="Guess", command=self.player_guess)
        self.guess_button.pack(pady=10)
        self.guess_button.config(state="disabled")

        self.feedback_label = ttk.Label(self.root, text="", font=("Arial", 12))
        self.feedback_label.pack(pady=10)

        self.score_label = ttk.Label(self.root, text="Score - Player: 0 | AI: 0", font=("Arial", 11, "bold"))
        self.score_label.pack(pady=10)

    def start_game(self):
        self.attempts = 0
        self.feedback_label.config(text="")
        self.entry.config(state="normal")
        self.guess_button.config(state="normal")
        self.start_button.config(state="disabled")
        self.current_turn = "Player"

        difficulty = self.difficulty.get()
        if difficulty == "Easy":
            self.range_min, self.range_max = 1, 10
        elif difficulty == "Medium":
            self.range_min, self.range_max = 1, 50
        else:
            self.range_min, self.range_max = 1, 100

        self.target_number = random.randint(self.range_min, self.range_max)
        self.ai_guess_low = self.range_min
        self.ai_guess_high = self.range_max

        self.status_label.config(text=f"Player's Turn – Guess a number between {self.range_min} and {self.range_max}")

    def player_guess(self):
        try:
            guess = int(self.entry.get())
        except ValueError:
            messagebox.showwarning("⚠️ Invalid Input", "Please enter a valid number.")
            return

        self.attempts += 1
        if guess < self.target_number:
            feedback = "🔻 Too low!"
        elif guess > self.target_number:
            feedback = "🔺 Too high!"
        else:
            self.player_score += 1
            messagebox.showinfo("🎉 Correct!", f"You guessed it right in {self.attempts} attempts!")
            return self.reset_game()

        self.feedback_label.config(text=f"Player: {feedback}")
        self.current_turn = "AI"
        self.status_label.config(text="AI's Turn...")
        self.entry.delete(0, tk.END)
        self.root.after(1000, self.ai_turn)

    def ai_turn(self):
        if self.ai_guess_low > self.ai_guess_high:
            messagebox.showinfo("Game Over", f"AI failed to guess the number. It was {self.target_number}.")
            return self.reset_game()

        guess = (self.ai_guess_low + self.ai_guess_high) // 2
        self.attempts += 1

        if guess < self.target_number:
            self.ai_guess_low = guess + 1
            feedback = f"🤖 AI guessed {guess}: Too low!"
        elif guess > self.target_number:
            self.ai_guess_high = guess - 1
            feedback = f"🤖 AI guessed {guess}: Too high!"
        else:
            self.ai_score += 1
            messagebox.showinfo("❌ AI Wins", f"AI guessed it correctly in {self.attempts} attempts!")
            return self.reset_game()

        self.feedback_label.config(text=feedback)
        self.current_turn = "Player"
        self.status_label.config(text=f"Player's Turn – Guess a number between {self.range_min} and {self.range_max}")

    def reset_game(self):
        self.score_label.config(text=f"Score - Player: {self.player_score} | AI: {self.ai_score}")
        self.entry.config(state="disabled")
        self.guess_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.status_label.config(text="")
        self.feedback_label.config(text="")
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()

