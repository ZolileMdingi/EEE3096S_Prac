import time
import busio
import digitalio
import board
import RPi.GPIO as GPIO
from adafruit_debouncer import Debouncer
import threading
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI) #setup SPI 
cs = digitalio.DigitalInOut(board.D8) #set up CS/SHDN pin at GPIO pin 8

#setup button
button = digitalio.DigitalInOut(board.D16) #setup button at GPIO 16
button.direction = digitalio.Direction.INPUT #set as input
button.pull = digitalio.Pull.UP #enable pull up resistor
switch = Debouncer(button) #add to adafruit debouncing assistant object
#thread resource establishment
stop_thread = False #thread flag
lock = threading.Lock() #lock for mutual exclusion

mcp = MCP.MCP3008(spi, cs) #create MCP3008 instnace to interface with 
ldr_channel = AnalogIn(mcp, MCP.P2) #interface MCP3008 instnace with channel 2 device(ldr)
temp_channel = AnalogIn(mcp, MCP.P1)#interface MCP3008 instnace with channel 1 device(temp sensor)
seconds_change = 10 #default runtime change

#convert temp sensor reading to degrees celsius
def temp_in_C(voltageVal):
    ADC_VREF = 5 #vref
    MCP9700_T_COEFF = 0.01 #in datasheet
    MCP9700_OFFSET = 0.5#also in datasheet
    return (voltageVal-MCP9700_OFFSET)/MCP9700_T_COEFF # degree celsuis 

#setup thread 
def run_thread(): 
     thread = threading.Thread(target=app,args=(temp_channel,ldr_channel,)) #create thread and function it to run
     thread.start() #begin paralel execution
#function that performs the operation within the thread
def app(temp_channel, ldr_channel):
    global seconds_change
    global stop_thread
    second = 0
    init_second_val = time.time() #time execution begins
    print("{:<7s} \t {:<12s} \t{:<4s}  \t{:<12s}".format("Runtime","Temp Reading","Temp","Light Reading"))
    # print("Runtime".ljust(7),'\t{:<12}'.format(temp_channel.value),'\t','{:<4.2f}'.format(temp_in_C(temp_channel.voltage)),'C \t',"{:<9.2f}".format(ldr_channel.value))
    while not stop_thread: #while thread not stopped
        print((str(round(second))+'s').ljust(7),'\t{:<12.2f}'.format(temp_channel.value),'\t','{:<4.2f}'.format(temp_in_C(temp_channel.voltage)),'C \t',"{:<12.2f}".format(ldr_channel.value))  
        with lock:#prevent changes to seconds_change and second to occur while executing statements by other threads
            time.sleep(seconds_change) #delay by the time in 'seconds change' var
            second =time.time() - init_second_val #calculate time for next reading.
def change_secs():
    global lock
    global seconds_change
    with lock: #mutual exclusion, thread has sole access to resources
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
        while(True): #pool button till program ended
            switch.update()
            if switch.fell == True: #button pressed
                change_secs() #change sampling rate 
                time.sleep(0.5) #debounce
    except KeyboardInterrupt:
        stop_thread = True #press control c to stop program, this sets stop thread to true and reading thread  stops
     


if __name__ == "__main__":
    main()