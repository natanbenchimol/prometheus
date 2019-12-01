import threading
import random
import time

# File is just used to test different validity/speeds of different syntaxes
# Used during development and during code optimisation

def printNum(num):
    time.sleep(random.randint(0, 5))
    print(num)

def main():

    # Test here

    print("All done")

main()