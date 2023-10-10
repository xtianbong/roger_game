import random
import keyboard
import time

def main():
    key_mapping = {1: '1', 2: '2', 3: '3'}
    score = 0
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
                score = 0
        except KeyboardInterrupt:
            break
        #give the user time to take their finger off the input
        time.sleep(3)

if __name__ == "__main__":
    main()