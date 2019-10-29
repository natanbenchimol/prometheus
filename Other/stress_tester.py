import math
import time
import multiprocessing

# Creates 4 processes, each of which finds the sum of all primes < 10 million

def sum_of_primes(proc_num, max):
    num = 2
    sum = 0

    # 10 million
    while num < max:
        div = 2
        sqrt = math.sqrt(num)
        isPrime = True

        while div < sqrt+1:       # Primality test by looping thru all numbers from 2 - sqrt(n)
            if num % div == 0:
                isPrime = False
                break
            div += 1

        # if isPrime:             # If isPrime hasnt been set to false, num is a prime
        #     sum += num

        num += 1

        if num%100000 == 0:
            print(str(proc_num) + ": " + str(num))

    print("Process " + str(proc_num) +  " final sum: " + str(num))


def main():

    NUM_PROCS = 8
    MAX_NUM = 4000000

    procs = []

    for i in range(NUM_PROCS):
        p1 = multiprocessing.Process(target=sum_of_primes, args=[i+1, MAX_NUM])
        procs.append(p1)

    t0 = time.time()

    for proc in procs:
        proc.start()

    for proc in procs:
        proc.join()

    t1 = time.time()
    total = t1 - t0

    print("Total elapsed time: " + str(int(total//60)) + "m" + str(int(total%60)) + "s")


main()
