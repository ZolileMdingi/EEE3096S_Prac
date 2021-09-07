import RPi.GPIO as GPIO 
import time
from random import randint

# generating random number between [0, 7]
random_generated_number = randint(0,7)
GPIO.cleanup() # cleaning up after the pins
GUESS_BTN = 23 # GPIO pin number
SUBMIT_GUESS = 24 # GPIO pin number
GPIO.setmode(GPIO.BCM) # Board mode

# setting up GPIO pin 24 as input pin
GPIO.setup(SUBMIT_GUESS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# setting up GPIO pin 23 as input pin
GPIO.setup(GUESS_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#print(GPIO.input(23))

#print(not GPIO.input(23))
LEDS = [17,27,22] # GPIO pins for the three Green LEDS that indicate user guess number
GPIO.setup(LEDS, GPIO.OUT) # setting the LED pins as output pins
print("the random number is ",random_generated_number)

# whats going on here I assume you were just testing something??
while not GPIO.input(23) == GPIO.LOW:
    GPIO.output(LEDS, GPIO.HIGH)

print("button was pressed")
_guess = 0
PWM_LED = 12 # The Red LED for indicating if the value submitted is correct, also its controlled by PWM for brightness
BUZZER = 13 # GPIO pin for the buzzer
GPIO.setup(13,GPIO.OUT)
GPIO.output(13,0)
GPIO.setup(PWM_LED, GPIO.OUT)
pi_pwm = GPIO.PWM(PWM_LED, 1000) # The Frequency is set to 1000Hz for the LED pin
pi_pwm.start(100) # I am guessing this start the duty cycle at 100

#buzzer_pwm = GPIO.PWM(BUZZER, 2)
#time.sleep(0.5)
#buzzer_pwm.start(50)
#time.sleep(0.5)
#buzzer_pwm.ChangeFrequency(2)
# What does this do?
GPIO.add_event_detect(GUESS_BTN,GPIO.RISING)
GPIO.add_event_detect(SUBMIT_GUESS, GPIO.RISING)
try:
    while True:
            if GPIO.event_detected(23):
            #while not GPIO.input(23) == GPIO.LOW:
                    time.sleep(0.5) # I see you trying to handle debouncing so that you limit the noise
                    if _guess == 0:
                            GPIO.output([22,27,17], GPIO.LOW)

                    elif _guess == 1:
                            GPIO.output(22, GPIO.HIGH)
                    elif _guess == 2:
                            GPIO.output(27, GPIO.HIGH)
                            GPIO.output(22, GPIO.LOW)
                    elif _guess == 3:
                            GPIO.output([27, 22], GPIO.HIGH)
                    elif _guess == 4:
                            GPIO.output([27, 22], GPIO.LOW)
                            GPIO.output(17, GPIO.HIGH)
                    elif _guess == 5:
                            GPIO.output(22, GPIO.HIGH)
                    elif _guess == 6:
                            GPIO.output(22, GPIO.LOW) 
                            GPIO.output(27, GPIO.HIGH)
                    elif _guess == 7:
                            GPIO.output(22, GPIO.HIGH)
                    print(_guess)
                    if _guess < 7: 
                            _guess += 1
                            print("increment "+str(_guess))
                    else:
                            _guess = 0

            elif GPIO.event_detected(SUBMIT_GUESS):
                    #call the function which does the submissio
                    print(_guess)
                    print(random_generated_number)
                    if _guess == random_generated_number:
                            break
                    else:
                            dc = (abs(_guess-1-random_generated_number)*100)//random_generated_number
                            dc =  int(dc)
                            print(dc)
                            pi_pwm.ChangeDutyCycle(dc)
except KeyboardInterrupt:
    print("WE still here dawg")
    pass
                        #break
pi_pwm.stop()
        # pi_pwm = GPIO.PWM(12,1000)
# pi_pwm.start(0)

# try:

#     while 1:

#         while not GPIO.input(23)==GPIO.LOW:

#             pi_pwm.ChangeDutyCycle(100)
#             print("Duty cycle on 100")

#             time.sleep(0.1)

#         while not GPIO.input(23)==GPIO.LOW:

#             pi_pwm.ChangeDutyCycle(75)
#             print("Duty cycle on 75")
#             time.sleep(0.1)

#         while not GPIO.input(23)==GPIO.LOW:

#             pi_pwm.ChangeDutyCycle(50)
#             print("Duty cycle on 50")

#             time.sleep(0.1)

#         while not GPIO.input(23)==GPIO.LOW:

#             pi_pwm.ChangeDutyCycle(25)
#             print("Duty cycle on 25")
#             time.sleep(0.1)

# except KeyboardInterrupt:

#     pass

# pi_pwm.stop()


GPIO.cleanup()