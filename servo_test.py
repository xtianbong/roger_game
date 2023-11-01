from servo import half_spin
# Set the GPIO mode and pin
servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
half_spin()