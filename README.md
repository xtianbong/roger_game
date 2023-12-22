# roger_game

Enriching game for my cat to play in exchange for treats.

## Description

This project allows your cat to play a game and receive treats as a reward. The player is rewarded with treats (dispensed by a rotating servo) when they get 5 correct answers in a row.

## Requirements

- Raspberry Pi system
- Screen
- Wires
- 3 binary input devices of your choice (e.g., [pet communication buttons](https://a.co/d/i0OjBEy))

To connect the buttons, solder two wires on either side of the internal switch to get a signal when the button is pressed. Run the return signal through a 10,000 Ω resistor.

## Installation and Use

1. Clone this repository:

    ```
    git clone https://github.com/xtianbong/roger_game
    ```

2. Install prerequisites:

    ```
    pip install -r requirements.txt
    ```

3. Run the app:

    ```
    python gui.py
    ```

## Hardware Configuration

- BCM GPIO inputs (buttons): 13, 19, and 26 (default, can be changed in `gui.py` under imports)
- GPIO output (servo): 18
