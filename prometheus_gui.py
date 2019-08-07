# Prometheus Graphical User Interface V2
# By Atticus Vadera
# 7/23/2019
from sys import maxsize
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import prometheus_shared as shared
import prometheus_consts as CONST
import RPi.GPIO as GPIO

import time

# ------------------------------------------ initialize setup values --------------------------------------------------#
# set up input out put pin numbering system on Pi (BCM = broadcom chip specific)
# enter "pinout" in the pi's terminal to see it's numbers
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(10, GPIO.IN)

global font
global tog
tog = 1
font = 'ansi'
class PrometheusGUI:

    def __init__(self, parent):

        self.parent = parent
        parent.title('Prometheus GUI')
        shared.populate_live_data()  # FAKE ASS DATA

        # Atticus laptop directory
        # self.tog_off = Image.open(r"C:\Users\Atticus\Desktop\prometheus\Assets\toggle_off.png").resize((125, 50),
        #    Image.ANTIALIAS)

        # self.tog_on = Image.open(r"C:\Users\Atticus\Desktop\prometheus\Assets\toggle_on.png").resize((125, 50),
        #    Image.ANTIALIAS)

        # Pi directory

        self.tog_off = Image.open(r"/home/pi/Desktop/prometheus/Assets/toggle_off.png").resize((125, 50), Image.ANTIALIAS)

        self.tog_on = Image.open(r"/home/pi/Desktop/prometheus/Assets/toggle_on.png").resize((125, 50), Image.ANTIALIAS)

        # initiate
        self.toggle_off = ImageTk.PhotoImage(self.tog_off)

        self.toggle_on = ImageTk.PhotoImage(self.tog_on)


########################################################################################################################
# ----------------------------------------- initialize frame set up ---------------------------------------------------#
########################################################################################################################

        # initialize frame 1 (static panel, includes title, panel change buttons)
        self.f1 = tk.Frame(parent, background='#000000')
        self.f1.grid(sticky=(N, S, E, W))

        # initialize frame 2 (central panel side a - manual ops with valve control, side b - fire ops)
        self.f2 = tk.Frame(self.f1, background='#000000', borderwidth=1, relief="sunken", width=100, height=80)
        self.f2.grid(row=1, columnspan=3, rowspan=2, sticky=(N, S, E, W))

        # initialize frame 3 (right side panel side A readouts side B set aborts)
        self.f3 = tk.Frame(self.f1, background='#000000', relief="sunken", width=80)
        self.f3.grid(column=3, row=1, columnspan=2, rowspan=3, sticky=(N, S, E, W))  # added sticky

        # initialize frame 4 (static panel at bottom for firing parameters)
        self.f4 = tk.Frame(self.f1, background='#000000', relief="sunken", width=100)
        self.f4.grid(column=0, row=3, columnspan=3, sticky=(N, S, E, W))  # added sticky

# -------------------------- scaling factors for static frames, (non static frame scaling set below) ------------------#
        # parent (root)
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        # f1 (branch of root)
        for x in range(5):
            self.f1.columnconfigure(x, weight=1)
        self.f1.rowconfigure(0, weight=1)
        for x in range(1, 4):
            self.f1.rowconfigure(x, weight=4)

########################################################################################################################
# ------------------------------------- GUI LAYOUT, setup widgets here ------------------------------------------------#
########################################################################################################################

# ------------------------------- frame 1 (main labels and panel switches) --------------------------------------------#
        self.main_ops = tk.Button(self.f1, text="Manual Mode", font=(font, 20), bg='#FFD700', command=lambda: self.switch_2('Man'))
        self.main_ops.grid(column=0, row=0, sticky=(N, S, E, W))

        self.fire_ops = tk.Button(self.f1, text="Firing Mode", font=(font, 20), bg='#c41e3a', command=lambda: self.switch_2('Fire'))
        self.fire_ops.grid(column=2, row=0, sticky=(N, S, E, W))

        self.abort_ops = tk.Button(self.f1, text="Aborts Values", font=(font, 15), bg='#bc13fe', borderwidth='5', relief='ridge', command=lambda: self.switch_3('aborts'))
        self.abort_ops.grid(column=4, row=0, sticky=(N+E + S + W), padx=30, pady=10)
        self.sense_ops = tk.Button(self.f1, text="Readouts", font=(font, 15), bg='#fe019a', borderwidth='5', relief='ridge', command=lambda: self.switch_3('sense'))
        self.sense_ops.grid(column=3, row=0, sticky=(N + E+ W + S), padx=30, pady=10)


# ------------------------------------- frame 4 (set firing parameters) -----------------------------------------------#
# set grid size on frame 3 b (mostly for debugging and convenience of rearranging widgets)
        f4brow = 7
        f4bcolumn = 5
        for column in range(f4bcolumn):
            for row in range(f4brow):
                self.f4_grid = tk.Label(self.f4, bg='#000000')
                self.f4_grid.grid(column=column, row=row, sticky=(N, S, E, W))
        # scaling factor for frame4
        for x in range(f4bcolumn):
            self.f4.columnconfigure(x, weight=1)
        for x in range(f4brow):
            self.f4.rowconfigure(x, weight=1)

        # add widgets
        self.fire_param = tk.Label(self.f4, text="Firing Parameters", font=(font, 20, 'bold', 'underline'), bg='#000000',
                                   fg='#FFFFFF')
        self.fire_param.grid(column=0, row='0', sticky=(N, S, E, W))

        self.start_param = tk.Label(self.f4, text="Start", font=(font, 20, 'bold'), bg='#000000',
                                   fg='#FFFFFF')
        self.start_param.grid(column=1, row=1, sticky=(N, S, E, W))

        self.stop_param = tk.Label(self.f4, text="Stop", font=(font, 20, 'bold'), bg='#000000',
                                    fg='#FFFFFF')
        self.stop_param.grid(column=2, row=1, sticky=(N, S, E, W))

        self.progress_param = tk.Label(self.f4, text="Progress Bar", font=(font, 20, 'bold'), bg='#000000',
                                   fg='#FFFFFF')
        self.progress_param.grid(column=3, row=1,columnspan=2, sticky=(N, S, E, W))


        self.sequence_time = tk.Label(self.f4, text='Total Sequence Time', font=(font, 15, 'bold'), bg='#000000', fg='#FFFFFF')
        self.sequence_time.grid(column=0, row=2)

        self.sequence_prog = tk.Label(self.f4, font=(font, 15, 'bold'), bg='#FFFFFF',
                                      fg='#FFFFFF', borderwidth=10, relief='groove')
        self.sequence_prog.grid(column=3, row=2, columnspan=2, sticky=(N, S, W, E))

        self.spark_frequency = tk.Label(self.f4, text="Spark Frequency", font=(font, 15, 'bold'), bg='#000000',
                                      fg='#FFFFFF')
        self.spark_frequency.grid(column=0, row=3)

        self.spark_timing = tk.Label(self.f4, text="Spark Timing", font=(font, 15, 'bold'), bg='#000000',
                                        fg='#FFFFFF')
        self.spark_timing.grid(column=0, row=4)

        self.spark_prog = tk.Label(self.f4, font=(font, 15, 'bold'), bg='#FFFFFF',
                                      fg='#FFFFFF', borderwidth=10, relief='groove')
        self.spark_prog.grid(column=3, row=4, columnspan=2, sticky=(N, S, W, E))

        self.NC_IO_timing = tk.Label(self.f4, text="NCIO Timing", font=(font, 15, 'bold'), bg='#000000',
                                     fg='#FFFFFF')
        self.NC_IO_timing.grid(column=0, row=5)

        self.NCIO_prog = tk.Label(self.f4, font=(font, 15, 'bold'), bg='#FFFFFF',
                                      fg='#FFFFFF', borderwidth=10, relief='groove')
        self.NCIO_prog.grid(column=3, row=5, columnspan=2, sticky=(N, S, W, E))

        self.NC_IF_timing = tk.Label(self.f4, text="NCIF Timing", font=(font, 15, 'bold'), bg='#000000',
                                     fg='#FFFFFF')
        self.NC_IF_timing.grid(column=0, row=6)

        self.NCIF_prog = tk.Label(self.f4, font=(font, 15, 'bold'), bg='#FFFFFF',
                                      fg='#FFFFFF', borderwidth=10, relief='groove')
        self.NCIF_prog.grid(column=3, row=6, columnspan=2, sticky=(N, S, W, E))
# ----------------------------------- frame 2 (manual ops and firing ops) ---------------------------------------------#

    # this function controls the switch for frame2
    def switch_2(self, s2):
        global font

        if s2 == 'Man':
            switch2 = 'a'
        elif s2 == 'Fire':
            switch2 = 'b'
# -------------------------------------------- Manual panel options -------------------------------------------------- #

        if switch2 == 'a':

            # set grid size on frame 2 (mostly for debugging and convenience of rearranging widgets)

            f2arow = 4
            f2acolumn = 9
            self.f2 = tk.Frame(self.f1, background='#000000', borderwidth=1, relief="sunken", width=100, height=80)
            self.f2.grid(row=1, columnspan=3, rowspan=2, sticky=(N, S, E, W))

            for column in range(f2acolumn):
                for row in range(f2arow):
                    self.f2_grid = tk.Label(self.f2, bg='#000000')
                    self.f2_grid.grid(column=column, row=row, sticky=(N, S, E, W))
            # scaling factor for frame2
            for x in range(f2acolumn):
                self.f2.columnconfigure(x, weight=1)
            for x in range(f2arow):
                 self.f2.rowconfigure(x, weight=1)

        # place widgets
            self.main_ops = tk.Label(self.f1, text="Manual Mode", font=(font, 35, 'bold'), bg='#000000', fg='#FFFFFF')
            self.main_ops.grid(column=1, row='0', sticky=(N, S, W, E))

# use const file from repository to shrink this to single loop in the future

            self.NC_IO = tk.Button(self.f2, text="NCIO", font=(font, 20), bg='#FF0000', fg='#FFFFFF',  borderwidth=10,
                                   relief='ridge', command=lambda: self.solenoid(self.NC_IO))
            self.NC_IO.grid(column=8, row=2, sticky=(N, S, E, W))

            self.NC_IF = tk.Button(self.f2, text="NCIF", font=(font, 20), bg='#FF0000', fg='#FFFFFF', borderwidth=10,
                                   relief='ridge')
            self.NC_IF.configure(command=lambda: self.solenoid(self.NC_IF))
            self.NC_IF.grid(column=0, row=2, sticky=(N, S, E, W))

            self.NO_IP = tk.Button(self.f2, text="NOIP", font=(font, 20), bg='#FF0000', fg='#FFFFFF', borderwidth=10,
                                   relief='ridge', command=lambda: self.solenoid(self.NO_IP))
            self.NO_IP.grid(column=3, row=2, sticky=(N, S, E, W))

            self.NC_IP = tk.Button(self.f2, text="NCIP", font=(font, 20), bg='#FF0000', fg='#FFFFFF', borderwidth=10,
                                   relief='ridge', command=lambda: self.solenoid(self.NC_IP))
            self.NC_IP.grid(column=5, row=2, sticky=(N, S, E, W))

            self.NC_3O = tk.Button(self.f2, text="NC3O", font=(font, 20), bg='#FF0000', fg='#FFFFFF', borderwidth=10,
                                   relief='ridge', command=lambda: self.solenoid(self.NC_3O))
            self.NC_3O.grid(column=1, row=0, sticky=(N, S, E, W), padx=40, pady=40)

            self.NC_3N = tk.Button(self.f2, text="NC3N", font=(font, 20), bg='#FF0000', fg='#FFFFFF', borderwidth=10,
                                   relief='ridge', command=lambda: self.solenoid(self.NC_3N))
            self.NC_3N.grid(column=7, row=0, sticky=(N, S, E, W), padx=40, pady=40)

            self.NC_OP = tk.Button(self.f2, text="NCOP", font=(font, 20), bg='#FF0000', fg='#FFFFFF', borderwidth=10,
                                   relief='ridge', command=lambda: self.solenoid(self.NC_OP))
            self.NC_OP.grid(column=4, row=0, sticky=(N, S, E, W), padx=40, pady=40)

            self.arm_valves = tk.Button(self.f2, text="ARM Valves", font=(font, 15), bg='#ff7300', fg='#FFFFFF',
                                        borderwidth=20, relief='raised', command=lambda: self.arm_v())
            self.arm_valves.grid(column=4, row=1, sticky=(N, S, E, W), padx=40, pady=40)

# -------------------------------------------- Firing panel options -------------------------------------------------- #

        elif switch2 == 'b':
            # set grid size on frame 2 (mostly for debugging and convenience of rearranging widgets)
            f2brow = 10
            f2bcolumn = 9
            self.f2 = tk.Frame(self.f1, background='#000000', borderwidth=1, relief="sunken", width=100, height=80)
            self.f2.grid(row=1, columnspan=3, rowspan=2, sticky=(N, S, E, W))

            for column in range(f2bcolumn):
                for row in range(f2brow):
                    self.f2_grid = tk.Label(self.f2, bg='#000000')
                    self.f2_grid.grid(column=column, row=row, sticky=(N, S, E, W))
            # scaling factor for frame2
            for x in range(f2bcolumn):
                self.f2.columnconfigure(x, weight=1)
            for x in range(f2brow):
                self.f2.rowconfigure(x, weight=1)

        # place widgets
            self.fire_ops = tk.Label(self.f1, text="Firing Mode", font=(font, 35, 'bold'), bg='#000000', fg='#FFFFFF')
            self.fire_ops.grid(column=1, row='0', sticky=(N, S, W, E))

            self.abort_butt = tk.Button(self.f2, text="ABORT", font=(font, 18), bg='#FF0000', fg='#FFFFFF')
            self.abort_butt.grid(column=7, row=3, columnspan=1, rowspan=2, sticky=(N, S, E, W))

            self.fire_butt = tk.Button(self.f2, text="FIRE", font=(font, 20), bg='#ff7300', fg='#FFFFFF')
            self.fire_butt.grid(column=1, row=3, columnspan=1, rowspan=2, sticky=(N, S, E, W))

            self.prefire_1 = tk.Label(self.f2, text="Valves in correct states", font=(font, 15),
                                       bg='#000000', fg='#FFFFFF')
            self.prefire_1.grid(column=4, row=2, sticky=(N, S, E, W))

            self.prefire_2 = tk.Label(self.f2, text="Sensor readings nominal"
                                                     ,  bg='#000000', font=(font, 15), fg='#FFFFFF')
            self.prefire_2.grid(column=4, row=3, sticky=(N, S, E, W))

            self.prefire_3 = tk.Label(self.f2,
                                       text="Range admin notified",
                                       bg='#000000', font=(font, 15), fg='#FFFFFF')
            self.prefire_3.grid(column=4, row=4, sticky=(N, S, E, W))

            self.prefire_4 = tk.Label(self.f2,
                                       text="Range is clear",
                                       bg='#000000', font=(font, 15), fg='#FFFFFF')
            self.prefire_4.grid(column=4, row=5, sticky=(N, S, E, W))

            self.prefire_5 = tk.Label(self.f2,
                                       text="Go/No go",
                                       bg='#000000', font=(font, 15), fg='#FFFFFF')
            self.prefire_5.grid(column=4, row=6, sticky=(N, S, E, W))

            self.prefire_6 = tk.Label(self.f2,
                                       text="Send it",
                                       bg='#000000', font=(font, 15), fg='#FFFFFF')
            self.prefire_6.grid(column=4, row=7, sticky=(N, S, E, W))

            # pre fire toggle switches, put this in a loop when you get better at python

            self.name1 = tk.Button(self.f2,  bg='#000000', activebackground="#000000", image=self.toggle_off, height=60,
                                 width=135, highlightthickness=0, bd=0, command=lambda: self.prefire_toggle(self.name1))
            self.name1.grid(column=5, row=2, sticky=(N, S, E, W))

            self.name2 = tk.Button(self.f2, bg='#000000', activebackground="#000000", image=self.toggle_off, height=60,
                           width=135, highlightthickness=0, bd=0, command=lambda: self.prefire_toggle(self.name2))
            self.name2.grid(column=5, row=3, sticky=(N, S, E, W))

            self.name3 = tk.Button(self.f2, bg='#000000', activebackground="#000000", image=self.toggle_off, height=60,
                                   width=135, highlightthickness=0, bd=0, command=lambda: self.prefire_toggle(self.name3))
            self.name3.grid(column=5, row=4, sticky=(N, S, E, W))

            self.name4 = tk.Button(self.f2, bg='#000000', activebackground="#000000", image=self.toggle_off, height=60,
                                   width=135, highlightthickness=0, bd=0, command=lambda: self.prefire_toggle(self.name4))
            self.name4.grid(column=5, row=5, sticky=(N, S, E, W))

            self.name5 = tk.Button(self.f2, bg='#000000', activebackground="#000000", image=self.toggle_off, height=60,
                                   width=135, highlightthickness=0, bd=0, command=lambda: self.prefire_toggle(self.name5))
            self.name5.grid(column=5, row=6, sticky=(N, S, E, W))

            self.name6 = tk.Button(self.f2, bg='#000000', activebackground="#000000", image=self.toggle_off, height=60,
                                   width=135, highlightthickness=0, bd=0, command=lambda: self.prefire_toggle(self.name6))
            self.name6.grid(column=5, row=7, sticky=(N, S, E, W))


# ---------------------------------- frame 3 (read outs, a and aborts. b) ---------------------------------------------#
            # this function controls the switch for frame3

    def switch_3(self, s3):

        global font
        if s3 == 'sense':
            switch3 = 'a'
        elif s3 == 'aborts':
            switch3 = 'b'

# -------------------------------------------- Sensor Readout Panel -------------------------------------------------- #

        if switch3 == 'a':

            # set grid size on frame 3a (mostly for debugging and convenience of rearranging widgets)
            f3arow = 21
            f3acolumn = 3
            for column in range(f3acolumn):
                for row in range(f3arow):
                    self.f3_grid = tk.Label(self.f3, bg='#000000')
                    self.f3_grid.grid(column=column, row=row, sticky=(N, S, E, W))
            # scaling factor for frame2
            for x in range(f3acolumn):
                self.f3.columnconfigure(x, weight=1)
            for x in range(f3arow):
                self.f3.rowconfigure(x, weight=1)

        # place widgets

            self.sense_ops = tk.Label(self.f3, text="Sensor Readouts ", font=(font, 25), bg='#000000', fg='#FFFFFF')
            self.sense_ops.grid(column=0, row='0', columnspan=3, sticky=(N, S, E, W))

            self.FM_O = tk.Label(self.f3, text="Oxygen Flow Meter ", font=(font, 15), bg='#000000', fg='#FFFFFF')
            self.FM_O.grid(column=0, row='1', sticky=(N, S, E, W))

            FM_O_live = IntVar(value=shared.LIVE_DATA["FM_IO"])

            self.FM_O_read = tk.Label(self.f3, textvariable=FM_O_live, font=(font, 15), bg='#000000', fg='#FFFFFF')

            self.FM_O_read.grid(column=1, row=1, sticky=(N, S, E, W))

            self.FM_O_unit = tk.Label(self.f3, text="g/s", font=(font, 15), bg='#000000', fg='#FFFFFF')
            self.FM_O_unit.grid(column=2, row='1', sticky=(N, S, E, W))

            self.FM_F = tk.Label(self.f3, text="Fuel Flow Meter ", font=(font, 15), bg='#000000', fg='#FFFFFF')
            self.FM_F.grid(column=0, row='2', sticky=(N, S, E, W))

            FM_F_live = IntVar(value=shared.LIVE_DATA["FM_IF"])

            self.FM_F_read = tk.Label(self.f3, textvariable=FM_F_live, font=(font, 15), bg='#000000', fg='#FFFFFF')
            self.FM_F_read.grid(column=1, row='2', sticky=(N, S, E, W))

            self.FM_F_unit = tk.Label(self.f3, text="g/s", font=(font, 15), bg='#000000', fg='#FFFFFF')
            self.FM_F_unit.grid(column=2, row='2', sticky=(N, S, E, W))


            self.Input_10 = tk.Label(self.f3, text="GPIO 10 ", font=(font, 15), bg='#000000', fg='#FFFFFF')
            self.Input_10.grid(column=0, row=3, sticky=(N, S, E, W))

            Input_10_live = IntVar(GPIO.input(10))

            self.Input_10read = tk.Label(self.f3, textvariable=Input_10_live, font=(font, 15), bg='#000000', fg='#FFFFFF')
            self.Input_10read.grid(column=1, row=3, sticky=(N, S, E, W))

# ------------------------------------------------ Set Aborts panel -------------------------------------------------- #
        elif switch3 == 'b':
            # set grid size on frame 3 b (mostly for debugging and convenience of rearranging widgets)
            f3brow = 10
            f3bcolumn = 3
            for column in range(f3bcolumn):
                for row in range(f3brow):
                    self.f3_grid = tk.Label(self.f3, bg='#000000')
                    self.f3_grid.grid(column=column, row=row, sticky=(N, S, E, W))
            # scaling factor for frame2
            for x in range(f3bcolumn):
                self.f3.columnconfigure(x, weight=1)
            for x in range(f3brow):
                self.f3.rowconfigure(x, weight=1)

    # place widgets
            self.abort_ops = tk.Label(self.f3, text="Abort Gates ", font=(font, 25), bg='#000000', fg='#FFFFFF')
            self.abort_ops.grid(column=0, row='0', columnspan=3, sticky=(N, S, E, W))

            self.FM_O = tk.Label(self.f3, text="Oxygen Flow Meter ", font=(font, 15), bg='#000000', fg='#FFFFFF')
            self.FM_O.grid(column=0, row='1', sticky=(N, S, E, W))
            
########################################################################################################################
# --------- GUI functionality, setup widgets functions here see below section to add/subtract widgets -----------------#
########################################################################################################################

# manual switch function


# arm valve function
    def arm_v(self):

        if self.arm_valves.cget('bg') == '#ff7300':
            self.arm_valves.configure(bg='#00FF00', relief='sunken')
            global arm
            arm = 1
        elif self.arm_valves.cget('bg') == '#00FF00':
            self.arm_valves.configure(bg='#ff7300', relief='raised')
            arm = 2

# this function actuates solenoids and changes button color based on previous state

    def solenoid(self, solbutton):
        if arm == 1:
            if solbutton.cget('bg') == '#FF0000':
                GPIO.output(17, GPIO.HIGH)
                solbutton.configure(bg='#00FF00', relief='ridge')
                print(GPIO.input(10))
            elif solbutton.cget('bg') == '#00FF00':
                GPIO.output(17, GPIO.LOW)
                solbutton.configure(bg='#FF0000', relief='ridge')
                print(GPIO.input(10))

        elif arm == 0:
            pass

    def prefire_toggle(self, toggle):
        bck = str(toggle.cget('image'))
        print(bck)
        if bck == "pyimage1":
            toggle.configure(image=self.toggle_on)
        elif bck == "pyimage2":
            toggle.configure(image=self.toggle_off)

########################################################################################################################
# -------------------------------------------------- THE END ----------------------------------------------------------#
########################################################################################################################
# loop this shit tho
root = Tk()
my_gui = PrometheusGUI(root)
root.mainloop()

