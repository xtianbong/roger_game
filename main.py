import random
import keyboard
import time
import csv
import datetime
import os

def main():
    key_mapping = {1: '1', 2: '2', 3: '3'}
    score = 0
    highest_score = get_highest_score()

    if not os.path.isfile('scores.csv'):
        create_scores_file()

    while True:
        target_number = random.randint(1, 3)
        print("Target Number:", target_number)
        print("Score:", score)

        try:
            pressed_key = keyboard.read_event().name
            if pressed_key == key_mapping[target_number]:
                score += 100
                print("Correct! You scored 100 points.")
            else:
                print("Wrong key! Game over.")
                if score > highest_score:
                    highest_score = score
                    print("(Best)")
                save_score(score)
                score = 0
                print(f"Highest Score: {highest_score}")
                print("Press Space to reset...")
                keyboard.wait('space')
        except KeyboardInterrupt:
            break
        time.sleep(1)

def save_score(score):
    now = datetime.datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M")
    with open('scores.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date_time, score])

def get_highest_score():
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

def create_scores_file():
    with open('scores.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date/Time", "Score"])

if __name__ == "__main__":
    main()
