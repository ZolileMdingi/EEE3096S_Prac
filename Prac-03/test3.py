import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN)



GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print(GPIO.input(23))

print(not GPIO.input(23))

GPIO.setup([12,13,17,27,22], GPIO.OUT)

while not GPIO.input(23) == GPIO.LOW:

    GPIO.output([12, 13,17,27,22], GPIO.HIGH)

print("button was pressed")


_guess = 0

while True:
    while not GPIO.input(23)==GPIO.LOW:
        global _guess
        if _guess == 0:
            GPIO.output(LEDS, GPIO.LOW)
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

        if _guess < 0:
            _guess += 1
        else:
            _guess = 0


GPIO.cleanup()

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
