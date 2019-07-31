from tkinter import Tk, Label, Button

import RPi.GPIO as GPIO
# GPIO = None

import time

#
#   Authored by Swapnil
#   Code now depreciated and not used
#   Kept a part of the project for documentation's sake
#


class PrometheusMain:
    def __init__(self, master):
        self.master = master

        if GPIO:
            GPIO.setmode(GPIO.BOARD)

        master.title("PROMETHEUS | Liquid Propulsion Lab | USC")

        self.label = Label(master, text="Valve Actuators")
        self.label.pack()

        self.greet_button = Button(master, text="Actuate", command=self.actuate)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=self.exit_main)
        self.close_button.pack()

    def actuate(self):
        if GPIO:
            GPIO.setup(7, GPIO.OUT)
            GPIO.output(7, True)

    def exit_main(self):
        if GPIO:
            GPIO.cleanup()
        print("some")
        self.master.quit()


root = Tk()
my_gui = PrometheusMain(root)
root.mainloop()

# Hello this is Sean
