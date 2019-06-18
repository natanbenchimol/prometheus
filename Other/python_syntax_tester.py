import threading
import random
import time


def printNum(num):
    time.sleep(random.randint(0, 5))
    print(num)

def main():

    threads = []

    for i in range(8):
        t = threading.Thread(target=printNum, args=[i])
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print("All done")

main()