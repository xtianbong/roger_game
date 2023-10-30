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
    time.sleep(0.5)  # Allow time for the servo to move

def full_spin():
    
    try:
        pwm.start(0)  # Start PWM with a duty cycle of 0 (servo at 0 degrees)
        set_angle(360)

    except KeyboardInterrupt:
        # Exit the program when Ctrl+C is pressed
        pwm.stop()
        GPIO.cleanup()

full_spin()