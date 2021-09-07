# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os
import time

# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
pi_pwm = None
# DEFINE THE PINS USED HERE

LEDS = [17,27,22]
PWM_LED = 12
SUBMIT_BTN = 24
GUESS_TOGGLE = 23
BUZZER =13
eeprom = ES2EEPROMUtils.ES2EEPROM()
scores = []
eeprom_scores =[76, 106, 117, 3, 69, 117, 69, 6, 106, 116, 102, 9, 100, 101, 118, 10]
_guess = 0
value = 0
number_of_tries = 0
PWM_LED = 12


def btn_increase_pressed(channel):
    
    global _guess
    
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
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        #value = generate_number()
        value = 7
        print(value)
        while not end_of_game:
            pass
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))
    # print out the scores in the required format
    raw_data.sort(key=lambda x: x[1])
    for i in range(1,4):
        data = raw_data[i-1]
        print("{} - {} took {} guesses".format(i,data[0],data[1]))
    pass


# Setup Pins
def setup():
    global pi_pwm
    # Setup board mode
    GPIO.setmode(GPIO.BCM) # The Board has been set to the Broadcom set up, which is what the chip that powers the pi use.
    # Setup regular GPIO
    
    # LEDs 
    GPIO.setup(LEDS, GPIO.OUT)
    GPIO.output(LEDS, GPIO.LOW)
    #Buttons
    GPIO.setup(SUBMIT_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(GUESS_TOGGLE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(GUESS_TOGGLE,GPIO.FALLING, callback=btn_increase_pressed, bouncetime=500)
    GPIO.add_event_detect(SUBMIT_BTN,GPIO.FALLING, callback=btn_guess_pressed, bouncetime=500)
    # Setup PWM channels
    GPIO.setup(PWM_LED, GPIO.OUT)
    pi_pwm = GPIO.PWM(PWM_LED, 1000)
    pi_pwm.start(0)
    # Setup debouncing and callbacks
    pass

def getName(nameChars):
    name = ''
    for x in nameChars:
        name = name + chr(x)
    return name

# Load high scores
def fetch_scores():
    global eeprom_scores
    # get however many scores there are
    score_count = None
    # Get the scores
    # convert the codes back to ascii
    # return back the results
    # score_count = eeprom.read_block(0xff,1)[0]
    # scores_raw = eeprom.read_block(1,score_count*4)
    scores_raw = eeprom_scores
    scores = []
    for x in range(0, len(scores_raw),4):
        scores.append([getName(scores_raw[x:x+3]),scores_raw[x+3]])
    return score_count, scores

def toRaw():
    pass

# Save high scores
def save_scores(newScore):
    global eeprom_scores
    print("Saved scores", newScore)
    # fetch scores
    # include new score
    # sort
    # update total amount of scores
    # write new scores
    oldScoreCount, oldScore = fetch_scores()
    oldScore.append(newScore)
    oldScore.sort(key=lambda x: x[1])
    data_to_write = []
    for score in oldScore:
        for letter in score[0]:
            data_to_write.append(ord(letter))
        data_to_write.append(score[1])
    # clear the eeprom to write new data to it.
    eeprom_scores = data_to_write
    # eeprom.clear((oldScoreCount+1)*32)
    # eeprom.write_block(0xff, [oldScoreCount+1])
    # eeprom.write_block(1, data_to_write)
    print("save done")
    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)


# Increase button pressed
def btn_increase_pressed(channel):
    global _guess
    
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
        _guess = -1
    pass

#
def addScore(scores, newScore):
    scores.append(newScore)
    
# Guess button
def btn_guess_pressed(channel):
    global number_of_tries
    global _guess
    global eeprom_scores
    global value
    start_time = time.time()
    while GPIO.input(channel) == 0: # Wait for the button up
        pass
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
    if .1 <= buttonTime < 2:
        number_of_tries += 1
        if _guess ==0:
            _guess = 7 
        else:
            _guess -= 1
        if _guess == value:
                #disable LEDS
                GPIO.output(LEDS, GPIO.LOW)
                accuracy_leds()
                #disable buzzer
                #user name
                name = input("Enter your name: ")
                #fetch scores 
                #add name to the scores
                save_scores([name[:3],number_of_tries])
                end_of_game = True 
                print("Done with round")
                the_scores_count, the_scores = fetch_scores()
                print(the_scores)
                print(eeprom_scores)
                pass
                #store the scores on the eeprom
        else:
            GPIO.output([22,27,17], GPIO.LOW)
            _guess=0
            accuracy_leds()
    elif 2 <= buttonTime:
        end_of_game = True   
    print("game done")   
    pass


# LED Brightness
def accuracy_leds():
    global pi_pwm
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
    if _guess>value:
        brightness = ((8-_guess)/(8-value))
    elif value==0 and _guess!=value:
        brightness = (_guess)/8
    elif _guess<value:
        brightness = (8-value)/(8-_guess)
    elif _guess==value:
        brightness = 0
    dc = brightness*100
    print(dc)
    pi_pwm.ChangeDutyCycle(dc)
    pass

# Sound Buzzer
def trigger_buzzer():
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
    pass


if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        welcome()
        while True:
            print("starting")
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
