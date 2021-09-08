import RPi.GPIO as GPIO
from gpiozero.tones import Tone
from gpiozero import TonalBuzzer
from time import sleep
import math
GPIO.setwarnings(False)
# BuzzerPin = 13
buzzerPin = 33
buttonPin = 18
p = None
def setup():
  global buzzerPin
  global buttonPin
  global p
  print ('Program is starting...')
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(buzzerPin, GPIO.OUT)
  p = GPIO.PWM(buzzerPin, 1000)
  GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  p.start(0)
  sleep(0.5)

def alertor():
  p.start(100)
  p.ChangeDutyCycle(100)

def stopAlertor():
  p.stop()


def loop():
  while True:
    if GPIO.input(buttonPin)==GPIO.LOW:
      alertor()
      print ('buzzer on ...')
    else :
      stopAlertor()
      print ('buzzer off ...')
def destroy():
  GPIO.output(buzzerPin, GPIO.LOW)
  GPIO.cleanup()
if __name__ == '__main__':
  setup()
  try:
    loop()
  except KeyboardInterrupt:
    destroy()

# def beep(s):
#     tb = TonalBuzzer(BuzzerPin)
#     tb.play(Tone(frequency=880))
#     sleep(s)
#     tb.stop()
#     tb.close()