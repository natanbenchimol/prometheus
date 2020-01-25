import threading
import random
import time

# File is just used to test different validity/speeds of different syntaxes
# Used during development and during code optimisation

def printNum(num):
    time.sleep(random.randint(0, 5))
    print(num)

def main():

    toggle_states = {
        # TOG_NAME: (isEnabled, isOn)
        "toggle_1": [True, False],
        "toggle_2": [True, False],
        "toggle_3": [True, False],
        "toggle_4": [True, False],
        "toggle_5": [True, False],
        "toggle_6": [True, False],
        "fire": [False, False],
    }



    for key in toggle_states:
        toggle_states[key][0] = False
        print(key, toggle_states[key][0])



main()