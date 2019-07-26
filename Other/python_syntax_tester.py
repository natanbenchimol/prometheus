import threading
import random
import time


def printNum(num):
    time.sleep(random.randint(0, 5))
    print(num)

def main():

    list = [1,3,5,6]

    for i in range(len(list)):
        if list[i] is 3:
            list[i] = 4

    print(list)


    print("All done")

main()