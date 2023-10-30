import RPi.GPIO as GPIO
import time

# Set the GPIO mode and pin
servo_pin = 22  # Use GPIO pin 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Create a PWM object with a frequency of 50Hz (standard for servos)
pwm = GPIO.PWM(servo_pin, 50)

# Function to set the angle of the servo
def set_angle(angle):
    duty_cycle = 2.5 + 10 * angle / 180  # Convert angle to duty cycle (2.5% to 12.5%)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)  # Allow time for the servo to move

try:
    pwm.start(0)  # Start PWM with a duty cycle of 0 (servo at 0 degrees)
    while True:
        # Rotate the servo from 0 to 180 degrees
        for angle in range(0, 181, 10):
            set_angle(angle)
        # Rotate the servo back from 180 to 0 degrees
        for angle in range(180, -1, -10):
            set_angle(angle)

except KeyboardInterrupt:
    # Exit the program when Ctrl+C is pressed
    pwm.stop()
    GPIO.cleanup()

set_angle(90) #test