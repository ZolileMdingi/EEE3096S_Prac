# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os
import math
import time

# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
number_of_tries = 0
_guess = 0
value = 0
LED_PWM = None
BUZZER_PWM = None

#eeprom instance
eeprom = ES2EEPROMUtils.ES2EEPROM()

# DEFINE THE PINS USED HERE
LEDS = [11, 13, 15]
PWM_LED = 32
SUBMIT_BTN = 16
GUESS_TOGGLE = 18
BUZZER = 33


def btn_increase_pressed(channel):
    global _guess
    if _guess == 0:
        GPIO.output([11, 13, 15], GPIO.LOW)
    elif _guess == 1:
        GPIO.output(15, GPIO.HIGH)
    elif _guess == 2:
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(15, GPIO.LOW)
    elif _guess == 3:
        GPIO.output([13, 15], GPIO.HIGH)
    elif _guess == 4:
        GPIO.output([13, 15], GPIO.LOW)
        GPIO.output(11, GPIO.HIGH)
    elif _guess == 5:
        GPIO.output(15, GPIO.HIGH)
    elif _guess == 6:
        GPIO.output(15, GPIO.LOW) 
        GPIO.output(13, GPIO.HIGH)
    elif _guess == 7:
        GPIO.output(15, GPIO.HIGH)
    if _guess < 7: 
        _guess += 1
    else:
        _guess = 0
    pass

# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")

# Setup Pins
def setup():
    global LED_PWM 
    global BUZZER_PWM
    # Setup board mode
    GPIO.setmode(GPIO.BOARD) 
    
    # LEDs 
    GPIO.setup(LEDS, GPIO.OUT)
    GPIO.output(LEDS, GPIO.LOW)
    #Buttons
    GPIO.setup(SUBMIT_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GUESS_TOGGLE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Setup PWM channels
    GPIO.setup(PWM_LED, GPIO.OUT)
    LED_PWM = GPIO.PWM(PWM_LED, 1000)
    LED_PWM.start(0)

    GPIO.setup(BUZZER, GPIO.OUT)
    BUZZER_PWM = GPIO.PWM(BUZZER, 1)
    BUZZER_PWM.start(0)
    time.sleep(0.5)
    # Setup debouncing and callbacks
    GPIO.add_event_detect(GUESS_TOGGLE,GPIO.FALLING, callback=btn_increase_pressed, bouncetime=500)
    GPIO.add_event_detect(SUBMIT_BTN,GPIO.FALLING, callback=btn_guess_pressed, bouncetime=500)
    pass



# Print the game menu
def menu():
    global value
    global end_of_game
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
        menu()
    elif option == "P":
        setup()
        time.sleep(0.5)
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        value = generate_number()
        print("The guess is now 7(LEDs all on)")
        GPIO.output([11, 13, 15], GPIO.HIGH)
        while not end_of_game:
            pass
        welcome()
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")
    

# Guess button
def btn_guess_pressed(channel):
    global number_of_tries
    global _guess
    global eeprom_scores
    global value
    # get start time the button is pressed
    start_time = time.time()
    while GPIO.input(channel) == 0: # Wait for the button to be released
        pass
    # difference between button is pressed and released
    buttonTime = time.time() - start_time
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    # Compare the actual value with the user value displayed on the LEDs
    # Change the PWM LED
    # if it's close enough, adjust the buzzer
    # if it's an exact guess:
    # - Disable LEDs and Buzzer
    # - tell the user and prompt them for a name
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
    if .1 <= buttonTime < 2: #if button press is less than 2 seconds
        number_of_tries += 1 #number of guessess for current 
        
        #for our setup, we make this adjustment
        if _guess ==0:
            _guess = 7 
        else:
            _guess -= 1
        if _guess == value:
                #disable LEDS
                GPIO.output(LEDS, GPIO.LOW)
                #disable LED
                accuracy_leds()
                #disable buzzer
                trigger_buzzer()
                #user name
                name = input("Enter your name: ")
                
                #add name to the scores(first 3 letters)
                save_scores([name[:3],number_of_tries])
                end_of_game = False 
                #fetch scores 
                the_scores_count, the_scores = fetch_scores()
                #end game
                GPIO.cleanup()
                number_of_tries = 0
                time.sleep(0.5)
                menu()
                pass
                #store the scores on the eeprom
        else:
            print("The guess is now 7(LEDs all on)")
            GPIO.output([11, 13, 15], GPIO.HIGH)
            accuracy_leds()
            trigger_buzzer()
            _guess=0
    elif 2 <= buttonTime:
        end_of_game = False
        #shut buzzer down and turn LED off
        _guess = value
        accuracy_leds()
        trigger_buzzer()
        #end game
        number_of_tries = 0
        GPIO.cleanup()
        time.sleep(0.5)
        menu()
    pass


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))
    # print out the scores in the required format
    raw_data.sort(key=lambda x: x[1])#sort data
    if count>2:
        for i in range(1,4):
            data = raw_data[i-1] #get High score for ith winner
            print("{} - {} took {} guesses".format(i,data[0],data[1]))
    else:
        for i in range(1,count+1):
            data = raw_data[i-1]
            print("{} - {} took {} guesses".format(i,data[0],data[1]))
    pass




def getName(nameChars):
    name = ''
    for x in nameChars:
        name = name + chr(x)
    return name

# Load high scores
def fetch_scores():
    # get however many scores there are
    score_count = None
    # Get the scores
    # convert the codes back to ascii
    # return back the results
    score_count = eeprom.read_byte(0x00) #get number of scores
    # print("scores stored: ",score_count)
    time.sleep(0.5)
    scores_raw = eeprom.read_block(1,score_count*4) #read all data from eeprom
    # scores_raw = eeprom_scores
    scores = []
    for x in range(0, len(scores_raw),4):
        scores.append([getName(scores_raw[x:x+3]),scores_raw[x+3]])
    return score_count, scores



# Save high scores
def save_scores(newScore):
    # global eeprom_scores
    # fetch scores
    # include new score
    # sort
    # update total amount of scores
    # write new scores
    oldScoresCount, oldScores = fetch_scores()
    oldScores.append(newScore) #add the new score to the scores in the eeprom
    oldScores.sort(key=lambda x: x[1])
    data_to_write = [] #array to store <8bit values for each register in each block
    #convert data for storage in eeprom
    for score in oldScores:
        for letter in score[0]:
            data_to_write.append(ord(letter))
        data_to_write.append(score[1])
    # clear the eeprom to write new data to it.
    eeprom.clear((oldScoresCount+1)*4)
    time.sleep(0.1)
    #write number of scores
    eeprom.write_block(0x00, [oldScoresCount+1])
    time.sleep(0.1)
    #write scores to eeprom
    eeprom.write_block(1, data_to_write)
    print("Score for",newScore[0],"successfully saved")
    pass 


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)


# Increase button pressed
#
def addScore(scores, newScore):
    scores.append(newScore)
    


# LED Brightness
def accuracy_leds():
    global LED_PWM
    global _guess
    global value
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
    brightness = 0
    if _guess>value:
        brightness = ((8-_guess)/(8-value))
    elif value==0 and _guess!=value:
        brightness = (_guess)/8
    elif _guess<value and value!=0:
        brightness = _guess/value
    dc = brightness*100
    LED_PWM.ChangeDutyCycle(dc)
    if brightness == 0:
        dc = 0 
        LED_PWM.ChangeDutyCycle(dc)
        LED_PWM.stop()
    else:
        dc = brightness*100
        LED_PWM.ChangeDutyCycle(dc)
    pass
def buzzerAlert(buzzer_pwm):
    buzzer_pwm.start(50)
def buzzerStop(buzzer_pwm):
    buzzer_pwm.stop()
# Sound Buzzer
def trigger_buzzer():
    global _guess
    global value
    global BUZZER_PWM
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
    # print("guess ",_guess)
    # print("value ",value)
    if abs(_guess-value)==3:
        BUZZER_PWM.ChangeFrequency(1)
        time.sleep(0.5)
        buzzerAlert(BUZZER_PWM)
    elif abs(_guess-value)==2:
        BUZZER_PWM.ChangeFrequency(2)
        time.sleep(0.5)
        buzzerAlert(BUZZER_PWM)
    elif abs(_guess-value)==1:
        BUZZER_PWM.ChangeFrequency(4)
        time.sleep(0.5)
        buzzerAlert(BUZZER_PWM)
    else:
        #stop beeping
        buzzerStop(BUZZER_PWM)
    time.sleep(0.5)
    pass


if __name__ == "__main__":
    try:
        # Call setup function
        
        welcome()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
