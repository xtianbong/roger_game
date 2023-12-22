# roger_game


Enriching game for my cat to play in exchange for treats.

The player is rewarded with treats (dispensed by a rotating servo) when they get 5 correct answers in a row.

## Requirements

Requires a raspberry pi system, a screen, wires and 3 binary input devices of your choice.

I used these pet communication buttons: [https://a.co/d/i0OjBEy](https://a.co/d/i0OjBEy)

You can solder two wires on either side of the internal switch such that you get a signal when the button is pressed. Make sure to run the return signal through a 10,000 Ω resistor.

## Installation and use

Clone this repository:
'''
git clone https://github.com/xtianbong/roger_game
'''

Install prerequisites:
'''
pip install -r requirements.txt
'''

Run the app:
'''
python gui.py
'''

## Notes
BCM GPIO inputs (the buttons) are set to 13,19 and 26 by default. They can be changed in gui.py right under the impoorts.
GPIO output (the servo) is set to 18
