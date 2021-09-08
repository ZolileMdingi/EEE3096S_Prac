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
  p = GPIO.PWM(buzzerPin, 1)
  GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  p.start(0)

def alertor():
  p.start(50)
  for x in range(0,361):
    sinVal = math.sin(x * (math.pi / 180.0))    
    toneVal = 2000 + sinVal * 500
    p.ChangeFrequency(toneVal)
    sleep(0.001)

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