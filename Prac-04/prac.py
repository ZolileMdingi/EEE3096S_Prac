import time
import busio
import digitalio
import board
import RPi.GPIO as GPIO
from adafruit_debouncer import Debouncer
import threading
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D8)

button = digitalio.DigitalInOut(board.D16)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
switch = Debouncer(button)
stop_thread = False
mcp = MCP.MCP3008(spi, cs)
lock = threading.Lock()

ldr_channel = AnalogIn(mcp, MCP.P2)
temp_channel = AnalogIn(mcp, MCP.P1)
seconds_change = 10


def temp_in_C(voltageVal):
    ADC_VREF = 5
    MCP9700_T_COEFF = 0.01
    MCP9700_OFFSET = 0.5
    return (voltageVal-MCP9700_OFFSET)/MCP9700_T_COEFF


def run_thread():
     thread = threading.Thread(target=app,args=(temp_channel,ldr_channel,))
     thread.start()
def app(temp_channel, ldr_channel):
    global seconds_change
    global stop_thread
    second = 0
    init_second_val = time.time()
    print("{} \t {} \t {}   \t {}".format("Runtime","Temp Reading","Temp","Light Reading"))
    while not stop_thread:
        print(str(round(second)).ljust(6),'\t','{:<9.2f}'.format(temp_channel.value),'\t','{:<4.2f}'.format(temp_in_C(temp_channel.voltage)),'C \t',"{:<9.2f}".format(ldr_channel.value))       
        # print("{runningtime:<}s \t {temp_reading:<9.2f} \t {temmp:<4.2f} C \t {l_reading:<9.2f}".format(runningtime = round(second),temp_reading = temp_channel.value,temmp = temp_in_C(temp_channel.value,temp_channel.voltage),l_reading  = ldr_channel.value))
        with lock:
            time.sleep(seconds_change)
            second =time.time() - init_second_val
def change_secs():
    global lock
    global seconds_change
    with lock:
        if seconds_change == 10:
            seconds_change = 5
        elif seconds_change == 5:
            seconds_change = 1
        else:
            seconds_change = 10
def main():
    global stop_thread
    try:
        run_thread()
        while(True):
            switch.update()
            if switch.fell == True:
                change_secs()
                time.sleep(0.5)
    except KeyboardInterrupt:
        stop_thread = True
     


# print('Raw ADC Value: ', channel.value)
# print('ADC Voltage: ' + str(channel.voltage) + 'V')
#egfw


main()