import threading
import time
import statistics

def printA():
    avg = []
    prevTime = time.time()
    for i in range(15):
        time.sleep(.1125)
        avg.append(time.time() - prevTime)
        #print(time.time() - prevTime)
        prevTime = time.time()
        #print("a")
    print("A AVERAGE:" + str(statistics.mean(avg)))


def printB():
    avg = []
    prevTime = time.time()
    for i in range(15):
        time.sleep(0.5)
        avg.append(time.time() - prevTime)
        print(time.time() - prevTime)
        prevTime = time.time()
        print("\tb" )
    print("B AVERAGE:" + str(statistics.mean(avg)))



def main():
    t1 = threading.Thread(target=printA)
    t2 = threading.Thread(target=printB)

    while(True):
        choice = input("> ")
        if choice == "1":
            t1.start()
        if choice == "2":
            t2.start()
        if choice == "3":
            print("we out here")

main()
