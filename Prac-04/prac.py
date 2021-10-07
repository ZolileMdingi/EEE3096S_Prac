import time
import busio
import digitalio
import board
import RPi.GPIO as GPIO
import threading
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
lock = threading.Lock()
ldr_channel = AnalogIn(mcp, MCP.P2)
temp_channel = AnalogIn(mcp, MCP.P1)
seconds_change = 10

def button_setup(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(pin,GPIO.FALLING, callback=change_secs, bouncetime=500)


def temp_in_C(raw_temp,voltageVal):
    ADC_VREF = 5
    ADC_V_PER_COUNT = ADC_VREF/1024
    MCP9700_T_COEFF = 0.01
    MCP9700_OFFSET = 0.5
    voltage = raw_temp*ADC_V_PER_COUNT
    return (voltageVal-MCP9700_OFFSET)/MCP9700_T_COEFF


def run_thread():
     thread = threading.Thread(target=app,args=(temp_channel,ldr_channel,))
     thread.start()
def app(temp_channel, ldr_channel):
    global seconds_change
    second = 0
    init_second_val = time.time()
    print("{} \t {} \t {}   \t {}".format("Runtime","Temp Reading","Temp","Light Reading"))
    while(True):       
        print("{runningtime:<}s \t {temp_reading:<9.2f} \t {temmp:<4.2f} C \t {l_reading:<9.2f}".format(runningtime = round(second),temp_reading = temp_channel.value,temmp = temp_in_C(temp_channel.value,temp_channel.voltage),l_reading  = ldr_channel.value))
        with lock:
            time.sleep(seconds_change)
            second =time.time() - init_second_val
def change_secs():
    global lock
    global seconds_change
    with lock:
        if seconds_change == 10:
            seconds_change = 5
            return
        elif seconds_change == 5:
            seconds_change = 1
            return
        seconds_change = 10
        return
def main():
    print("here")
    try:
        button_setup(36)
        run_thread()
    except Exception as e:
        print(e)
        GPIO.cleanup()
    
    
     


# print('Raw ADC Value: ', channel.value)
# print('ADC Voltage: ' + str(channel.voltage) + 'V')
#egfw


main()