import RPi.GPIO as GPIO 
import time
from random import randint

random_generated_number = randint(0,7)
GPIO.cleanup()
GUESS_BTN = 23
SUBMIT_GUESS = 24
GPIO.setmode(GPIO.BCM)

GPIO.setup(SUBMIT_GUESS, GPIO.IN, pull_up_down=GPIO.PUD_UP)


GPIO.setup(GUESS_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#print(GPIO.input(23))

#print(not GPIO.input(23))
LEDS = [17,27,22]
GPIO.setup(LEDS, GPIO.OUT)
print("the random number is ",random_generated_number)
while not GPIO.input(23) == GPIO.LOW:
    GPIO.output(LEDS, GPIO.HIGH)

print("button was pressed")
_guess = 0
PWM_LED = 12
# BUZZER = 13
# GPIO.setup(13,GPIO.OUT)
# GPIO.output(13,0)
GPIO.setup(PWM_LED, GPIO.OUT)
pi_pwm = GPIO.PWM(PWM_LED, 1000)
pi_pwm.start(100)

# GPIO.add_event_detect(GUESS_BTN,GPIO.RISING)
GPIO.add_event_detect(SUBMIT_GUESS, GPIO.RISING)
def btn_increase_pressed(channel):
    global _guess
    if _guess < 7: 
        _guess += 1
        print("increment "+str(_guess))
    else:
        _guess = 0
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
    
GPIO.add_event_detect(GUESS_BTN,GPIO.FALLING, callback=btn_increase_pressed, bouncetime=500)
try:
    while True:
            if GPIO.event_detected(24):
            #while not GPIO.input(23) == GPIO.LOW:
                    time.sleep(0.5)
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

