import math
import time
import multiprocessing


# Function to be turned into a process in order to benchmark a processor
# Inputs:   'proc_num' is an identifier used for printing to console
#           'max' is the largest number we will test for primality
def primes_less_than(proc_id, max):

    num = 2     # First number to primality test

    while num < max:
        div = 2                   # Always start by trying to divide by 2
        sqrt = math.sqrt(num)

        while div < sqrt+1:       # Primality test by looping thru all numbers from 2 - sqrt(n)
            if num % div == 0:
                break
            div += 1

        # Next number
        num += 1

        # Print to measure progress
        if num % 100000 == 0:
            print("Process " + str(proc_id) + " factoring: " + str(num))


def main():

    NUM_PROCS = 4
    MAX_NUM = 3000000

    procs = []

    # Setting up processes
    for i in range(NUM_PROCS):
        p1 = multiprocessing.Process(target=primes_less_than, args=[i+1, MAX_NUM])
        procs.append(p1)

    # Timing execution time of all processes
    t0 = time.time()

    # Start number crunching
    for proc in procs:
        proc.start()

    # Wait for all processes to complete
    for proc in procs:
        proc.join()

    # More timing functions
    t1 = time.time()
    total = t1 - t0

    # Print time
    print("Total elapsed time: " + str(int(total//60)) + "m" + str(int(total%60)) + "s")


main()
