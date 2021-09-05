import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)


GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(12, GPIO.OUT)

pi_pwm = GPIO.PWM(12,1000)
pi_pwm.start(0)

try:

    while 1:

        while not GPIO.input(23)==GPIO.LOW:

            pi_pwm.ChangeDutyCycle(100)

            time.sleep(0.1)

        while not GPIO.input(23)==GPIO.LOW:

            pi_pwm.ChangeDutyCycle(75)

            time.sleep(0.1)

        while not GPIO.input(23)==GPIO.LOW:

            pi_pwm.ChangeDutyCycle(50)

            time.sleep(0.1)

        while not GPIO.input(23)==GPIO.LOW:

            pi_pwm.ChangeDutyCycle(25)

            time.sleep(0.1)

except KeyboardInterrupt:

    pass

pi_pwm.stop()

GPIO.cleanup()
