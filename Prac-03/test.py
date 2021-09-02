import RPi.GPIO as GPIO
from time import sleep #To be removed was just testing if my connections was correct

# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18

# LEDs 
GPIO.setup(LED_value, GPIO.OUT)
GPIO.setup(LED_accuracy, GPIO.OUT)
GPIO.output(LED_accuracy, False)
GPIO.output(LED_value, False)

#Buttons
GPIO.setup(btn_increase, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        GPIO.output(LED_value, not GPIO.input(btn_submit))
        sleep(0.1)
finally:
    GPIO.output(LED_value, False)
    GPIO.cleanup