import RPi.GPIO as GPIO
import time

# Set the GPIO mode and pin
servo_pin = 22 
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Create a PWM object with a frequency of 50Hz
pwm = GPIO.PWM(servo_pin, 50)

# Function to set the angle of the servo
def set_angle(angle):
    duty_cycle = 2.5 + 10 * angle / 180  # Convert angle to duty cycle (2.5% to 12.5%)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Allow time for the servo to move

def half_spin():
    
    try:
        pwm.start(0)  # Start PWM with a duty cycle of 0 (servo at 0 degrees)
        angle = 0
        while angle<180:
            set_angle(angle)
            angle+=10
    except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()

half_spin() #testing
GPIO.cleanup()