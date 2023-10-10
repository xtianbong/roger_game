import random
import tkinter as tk
import time
import csv
import datetime
import os

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Game")
        self.root.geometry("400x500")  # Set the window size
        
        self.key_mapping = {1: '1', 2: '2', 3: '3'}
        self.score = 0
        self.highest_score = self.get_highest_score()
        
        self.target_number = None
        self.game_over = False  # To track whether the game is over
        
        if not os.path.isfile('scores.csv'):
            self.create_scores_file()

        self.target_label = tk.Label(root, text="", font=("Arial", 36))
        self.target_label.pack()

        

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.score_label = tk.Label(root, text="Score: 0", font=("Arial", 16))
        self.score_label.pack()

        for i in range(1, 4):
            button = tk.Button(self.button_frame, text=str(i), font=("Arial", 16))
            button["command"] = lambda i=i: self.check_number(i)
            button.grid(row=0, column=i-1)

        self.game_over_label = tk.Label(root, text="", font=("Arial", 20))
        self.high_score_label = tk.Label(root, text="", font=("Arial", 16))

        self.next_round()
        self.bind_keys_to_buttons()  # Call the function to bind keys to buttons

    def bind_keys_to_buttons(self):
        for key, button in zip(self.key_mapping.values(), self.button_frame.winfo_children()):
            self.root.bind(key, lambda event, b=button: b.invoke())

    def next_round(self):
        if not self.game_over:
            self.target_number = random.randint(1, 3)
            self.target_label.config(text="" + str(self.target_number))
        
    def check_number(self, pressed_number):
        if not self.game_over:
            if self.target_number == pressed_number:
                self.score += 100
                self.score_label.config(text="Score: " + str(self.score))
                self.next_round()  # Start a new round
            else:
                if self.score > self.highest_score:
                    self.highest_score = self.score
                    self.high_score_label.config(text="Highscore: " + str(self.highest_score))
                self.score_label.config(text="Score: " + str(self.score))
                self.save_score(self.score)
                final_score = self.score  # Save the final score
                self.score = 0
                self.game_over = True
                self.target_label.grid_forget()  # Hide the game screen
                self.button_frame.grid_forget()
                if final_score > self.highest_score:
                    self.game_over_label.config(text="Game Over\nScore: " + str(final_score) + " (Best!)\nHighscore: " + str(self.highest_score) + "\nPress space to reset")
                else:
                    self.game_over_label.config(text="Game Over\nScore: " + str(final_score) + "\nHighscore: " + str(self.highest_score) + "\nPress space to reset")
                self.game_over_label.pack()

    def save_score(self, score):
        now = datetime.datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M")
        with open('scores.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date_time, score])

    def get_highest_score(self):
        try:
            with open('scores.csv', mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                scores = [(int(score), date) for date, score in reader]
                if scores:
                    highest = max(scores, key=lambda x: x[0])
                    return highest[0]
        except FileNotFoundError:
            pass
        return 0

    def create_scores_file(self):
        with open('scores.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date/Time", "Score"])

    def reset_game(self, event):
        if self.game_over and event.keysym == "space":
            self.game_over = False
            self.target_label.pack()  # Show the game screen
            self.button_frame.pack()
            self.game_over_label.pack_forget()  # Hide the game-over screen
            self.next_round()
            self.score = 0
            self.score_label.config(text="Score: 0")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.bind("<Key>", app.reset_game)  # Bind the reset function to the space key
    root.mainloop()
