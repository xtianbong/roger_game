import random
import tkinter as tk
import time
import csv
import datetime
import os
import pygame
import RPi.GPIO as GPIO

from PIL import Image, ImageTk  


# set up gpio pins
GPIO.setmode(GPIO.BCM)
pins = [13, 19, 26]

for pin in pins:
    GPIO.setup(pin, GPIO.IN)

bg_color = "#D3D3D3"

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Game")
        self.root.geometry("400x500")  # Set the window size
        
        
        
        self.key_mapping = {1: '1', 2: '2', 3: '3'}
        self.score = 0
        self.highest_score = self.get_highest_score()
        
        self.target_number = random.randint(1, 3)
        self.game_over = False  # To track whether the game is over
        self.flash_duration = 500  # 500 milliseconds (0.5 seconds)
        
        if not os.path.isfile('scores.csv'):
            self.create_scores_file()

        
        # load the image and create a PhotoImage object
        self.birdImg = Image.open("img/bird.png").convert("RGBA")
        self.mouseImg = Image.open("img/mouse.png").convert("RGBA")
        self.spiderImg = Image.open("img/spider.png").convert("RGBA")
        self.birdImg = self.birdImg.resize((150, 150))
        self.mouseImg = self.mouseImg.resize((150, 150))
        self.spiderImg = self.spiderImg.resize((150, 150))

        #choose image based on the target number
        if self.target_number == 1:
            self.photo = ImageTk.PhotoImage(self.spiderImg)
        if self.target_number == 2:
            self.photo = ImageTk.PhotoImage(self.birdImg)
        if self.target_number == 3:
            self.photo = ImageTk.PhotoImage(self.mouseImg)

        # create a label to display the image 
        self.image_label = tk.Label(root, image=self.photo,bg=bg_color)
        self.image_label.pack()
        self.image_label.place(x=125, y=150)

        self.update_image()  # Initial image update
        

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

        self.game_over_label = tk.Label(root, text="", font=("Arial", 20),borderwidth=3 , relief="solid",padx=5)
        self.high_score_label = tk.Label(root, text="", font=("Arial", 16))

        pygame.mixer.init()  # Initialize the mixer for sound effects

        # Set up GPIO event detection for button presses 42
        for pin in pins:
            GPIO.setup(pin, GPIO.IN)
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.handle_button_press, bouncetime=200)

        
        self.next_round()
        self.bind_keys_to_buttons()  # Call the function to bind keys to buttons

    def bind_keys_to_buttons(self):
        for key, button in zip(self.key_mapping.values(), self.button_frame.winfo_children()):
            self.root.bind(key, lambda event, b=button: b.invoke())

    def handle_button_press(self, channel):
        if not self.game_over:
            button_number = pins.index(channel) + 1
            self.check_number(button_number)


    def next_round(self):
        if not self.game_over:
            self.target_number = random.randint(1, 3)
            self.update_image()
            self.target_label.config(text="" + str(self.target_number))

    def update_image(self):
        if self.target_number == 1:
            image = ImageTk.PhotoImage(self.spiderImg)
        elif self.target_number == 2:
            image = ImageTk.PhotoImage(self.birdImg)
        elif self.target_number == 3:
            image = ImageTk.PhotoImage(self.mouseImg)
        else:
            image = ImageTk.PhotoImage(self.mouseImg) #default image

        self.image_label.configure(image=image)
        self.image_label.configure(bg=bg_color)
        self.image_label.image = image  # Keep a reference to avoid garbage collection

        
    def check_number(self, pressed_number):
        if not self.game_over:
            if self.target_number == pressed_number:
                self.score += 100
                self.score_label.config(text="Score: " + str(self.score))
                self.flash_screen_and_labels("green")  # Flash green for correct answer
                self.root.after(self.flash_duration, self.next_round)  # Start a new round after flashing
                self.play_sound_effect("sfx/success/1.mp3")
            else:
                if self.score > self.highest_score:
                    self.highest_score = self.score
                    self.flash_screen_and_labels("red")  # Flash red for wrong answer
                else:
                    self.save_score(self.score)
                    final_score = self.score  # Save the final score
                    self.score = 0
                    self.game_over = True
                    self.target_label.grid_forget()  # Hide the game screen
                    self.button_frame.grid_forget()
                    self.flash_screen_and_labels("red")  # Flash red for wrong answer
                    if final_score > self.highest_score:
                        self.game_over_label.config(text="Game Over\nScore: " + str(final_score) + " (Best!)\nHighscore: " + str(self.highest_score) + "\nPress space to reset", font=("Arial", 30))
                        self.root.after(self.flash_duration, self.display_game_over)
                    else:
                        self.game_over_label.config(text="Game Over\nScore: " + str(final_score) + "\nHighscore: " + str(self.highest_score) + "\nPress space to reset", font=("Arial", 30))
                        self.root.after(self.flash_duration, self.display_game_over)
                    self.play_sound_effect("sfx/failure/1.mp3")

    def flash_screen_and_labels(self, color):
        # Flash the screen
        self.root.configure(bg=color)
        # Flash the text labels
        self.target_label.configure(bg=color)
        self.score_label.configure(bg=color)
        self.high_score_label.configure(bg=color)
        self.image_label.configure(bg=color)
        self.root.update()
        if color == "green":
            self.root.after(self.flash_duration, self.reset_background)
    
    def reset_background(self):
        # Reset the background color to SystemButtonFace
        self.root.configure(bg=bg_color)
        self.target_label.configure(bg=bg_color)
        self.score_label.configure(bg=bg_color)
        self.high_score_label.configure(bg=bg_color)
        self.image_label.configure(bg=bg_color)

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

    def display_game_over(self):
        self.root.configure(bg="red")  # Set the background to red for game over
        self.target_label.configure(bg="red")
        self.score_label.configure(bg="red")
        self.high_score_label.configure(bg="red")
        self.game_over_label.pack()

    def reset_game(self, event):
        self.root.configure(bg=bg_color)  # Revert the background to white
        self.target_label.configure(bg=bg_color)
        self.score_label.configure(bg=bg_color)
        self.high_score_label.configure(bg=bg_color)
        self.game_over = False
        self.target_label.pack()  # Show the game screen
        self.button_frame.pack()
        self.game_over_label.pack_forget()  # Hide the game-over screen
        self.next_round()
        self.score = 0
        self.score_label.config(text="Score: 0")

    def play_sound_effect(self, sound_file):
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.bind("<space>", app.reset_game)  # Bind the reset function to the space key
    root.bind("<Escape>",app.close_game)
    root.mainloop()