import RPi.GPIO as GPIO
import time

# Set the GPIO mode and pins
GPIO.setmode(GPIO.BCM)
pins = [16, 20, 21]

# Set the pins as inputsxs
for pin in pins:
    GPIO.setup(pin, GPIO.IN)

try:
    while True:
        # Read the state of each pin
        pin_states = [GPIO.input(pin) for pin in pins]

        # Print the states (0 for OFF, 1 for ON)
        print("States:", pin_states)

        # You can also perform any other actions based on pin_states here

        # Wait for a short duration to avoid excessive CPU usage
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Clean up and release the GPIO pins
    GPIO.cleanup()
