# Prometheus Graphical User Interface V2
# By Atticus Vadera
# 7/23/2019

# Library Imports
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
# import RPi.GPIO as GPIO

# Internal Imports
import prometheus_shared as shared
import prometheus_daq as daq
from SolenoidManagerClass import SolenoidManager

# ------------------------------------------ initialize setup values --------------------------------------------------#
# set up input out put pin numbering system on Pi (BCM = broadcom chip specific)
# enter "pinout" in the pi's terminal to see it's numbers
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(17, GPIO.OUT)
# GPIO.setup(10, GPIO.IN)

global font
global tog
tog = 1
font = 'ansi'


class PrometheusGUI:

    def __init__(self, parent):

        self.parent = parent
        parent.title('Prometheus GUI')

        shared.init_live_data()  # Creates int values for all keys
        shared.populate_live_data()  # FILLS WITH FAKE ASS DATA
        self.SolManager = SolenoidManager()  # Initialize the solenoid manager

        self.prom_status = {
            "is_running": True,  # Variable read by batch_reader func
            "all_systems_go": False,  # Variable read by this function
            "should_record_data": False,  # Variable read by single_reader func
            "overdrive": False,  # Variable read by batch_reader func
            "did_abort": False,  # Variable read by logfile
            "countdown_start": None  # Variable read by logfile + reader funcs, set when we start recording
        }

        self.toggle_states = {
            # TOG_NAME: (isEnabled, isOn)
            "toggle_1": [True, False],
            "toggle_2": [False, False],
            "toggle_3": [False, False],
            "toggle_4": [False, False],
            "toggle_5": [False, False],
            "toggle_6": [False, False],
            "fire": [False, False]
        }
        
        self.next_toggle = {
            "toggle_1": "toggle_2",
            "toggle_2": "toggle_3",
            "toggle_3": "toggle_4",
            "toggle_4": "toggle_5",
            "toggle_5": "toggle_6",
            "toggle_6": "fire"
        }

        # START THE BACKEND CODE, BEGIN SHOWING LIVE VALS
        # daq.run_daq(sol, prom_status)

        # load pictures for check list buttons
        self.tog_off = Image.open(r"Assets/toggle_off.png").resize((125, 50), Image.ANTIALIAS)
        self.tog_on = Image.open(r"Assets/toggle_on.png").resize((125, 50), Image.ANTIALIAS)
        self.toggle_off = ImageTk.PhotoImage(self.tog_off)
        self.toggle_on = ImageTk.PhotoImage(self.tog_on)

        ###################################################################################
        # --------------------------- initialize frame set up --------------------------- #
        ###################################################################################

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

        # ------------------ scaling factors for static frames, (non static frame scaling set below) ------------------#
        # parent (root)
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        # f1 (branch of root)
        for x in range(5):
            self.f1.columnconfigure(x, weight=1)
        self.f1.rowconfigure(0, weight=1)
        for x in range(1, 4):
            self.f1.rowconfigure(x, weight=4)

        #########################################################################################
        # --------------------------- GUI LAYOUT, setup widgets here ---------------------------#
        #########################################################################################

        # --------------------------- frame 1 (main labels and panel switches) ---------------------------#
        self.main_ops = tk.Button(self.f1, text="Manual Mode", font=(font, 20), bg='#FFD700',
                                  command=lambda: self.switch_2('manual'))
        self.main_ops.grid(column=0, row=0, sticky=(N, S, E, W))

        self.fire_ops = tk.Button(self.f1, text="Firing Mode", font=(font, 20), bg='#c41e3a',
                                  command=lambda: self.switch_2('fire'))
        self.fire_ops.grid(column=2, row=0, sticky=(N, S, E, W))

        self.abort_ops = tk.Button(self.f1, text="Aborts Values", font=(font, 15), bg='#bc13fe', borderwidth='5',
                                   relief='ridge', command=lambda: self.switch_3('aborts'))
        self.abort_ops.grid(column=4, row=0, sticky=(N + E + S + W), padx=30, pady=10)

        self.sense_ops = tk.Button(self.f1, text="Readouts", font=(font, 15), bg='#fe019a', borderwidth='5',
                                   relief='ridge', command=lambda: self.switch_3('readouts'))
        self.sense_ops.grid(column=3, row=0, sticky=(N + E + W + S), padx=30, pady=10)

        # --------------------------- frame 4 (set firing parameters) ---------------------------#
        # set grid size on frame 3 b (mostly for debugging and convenience of rearranging widgets)
        f4brow = 6
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

        # add Labels/Headers
        self.fire_param = tk.Label(self.f4, text="Firing Parameters", font=(font, 20, 'bold', 'underline'),
                                   bg='#000000',
                                   fg='#FFFFFF')
        self.fire_param.grid(column=0, row=0, sticky=(N, S, E, W))

        self.start_header = tk.Label(self.f4, text="Start", font=(font, 20, 'bold', 'underline'), bg='#000000',fg='#FFFFFF')
        self.start_header.grid(column=1, row=2, sticky=(N, S, E, W))

        self.stop_header = tk.Label(self.f4, text="Stop", font=(font, 20, 'bold', 'underline'), bg='#000000', fg='#FFFFFF')
        self.stop_header.grid(column=2, row=2, sticky=(N, S, E, W))

        self.spark_frequency_lbl = tk.Label(self.f4, text="Spark Frequency (Hz)", font=(font, 15, 'bold'), bg='#000000',
                                            fg='#FFFFFF')
        self.spark_frequency_lbl.grid(column=0, row=1)

        self.spark_timing_lbl = tk.Label(self.f4, text="Spark Timing", font=(font, 15, 'bold'), bg='#000000',
                                         fg='#FFFFFF')
        self.spark_timing_lbl.grid(column=0, row=3)

        self.NC_IO_timing_lbl = tk.Label(self.f4, text="NCIO Timing", font=(font, 15, 'bold'), bg='#000000',
                                         fg='#FFFFFF')
        self.NC_IO_timing_lbl.grid(column=0, row=4)

        self.NC_IF_timing_lbl = tk.Label(self.f4, text="NCIF Timing", font=(font, 15, 'bold'), bg='#000000',
                                         fg='#FFFFFF')
        self.NC_IF_timing_lbl.grid(column=0, row=5)

        # Inputs

        self.spark_freq_input = tk.Entry(self.f4, width=10, font=(font, 9))
        self.spark_freq_input.grid(row=1, column=1)

        self.start_spark = tk.Entry(self.f4, width=10, font=(font, 9))
        self.start_spark.grid(row=3, column=1)

        self.stop_spark = tk.Entry(self.f4, width=10, font=(font, 9))
        self.stop_spark.grid(row=3, column=2)

        self.start_NCIO = tk.Entry(self.f4, width=10, font=(font, 9))
        self.start_NCIO.grid(row=4, column=1)

        self.stop_NCIO = tk.Entry(self.f4, width=10, font=(font, 9))
        self.stop_NCIO.grid(row=4, column=2)

        self.start_NCIF = tk.Entry(self.f4, width=10, font=(font, 9))
        self.start_NCIF.grid(row=5, column=1)

        self.stop_NCIF = tk.Entry(self.f4, width=10, font=(font, 9))
        self.stop_NCIF.grid(row=5, column=2)

        self.entry_list = [self.start_spark, self.stop_spark,
                           self.start_NCIO, self.stop_NCIO,
                           self.start_NCIF, self.stop_NCIF]

        self.load_vals = tk.Button(self.f4, text="Load Values", font=(font, 15), borderwidth='5',
                                   relief='ridge',command=lambda: self.save_timings())
        self.load_vals.grid(column=3, row=3)


    # Goes through the values inputted on the frontend and saves them to backend data structures
    def save_timings(self):
        print("YUH")

        shared.set_timing(self.start_spark.get(), "SPARK_1")
        shared.set_timing(self.stop_spark.get(), "SPARK_0")

        shared.set_timing(self.start_NCIO.get(), "NCIO_1")
        shared.set_timing(self.stop_NCIO.get(), "NCIO_0")

        shared.set_timing(self.start_NCIF.get(), "NCIF_1")
        shared.set_timing(self.stop_NCIF.get(), "NCIF_0")


    # -------------------------------- frame 2 -----------------------------------------#
    # Toggles frame 2 between Manual/Firing Ops
    def switch_2(self, desired_display):

        if desired_display == 'manual':
            self.init_manual()

        elif desired_display == 'fire':
            self.init_fire()

    # --------------------------- frame 3 (read outs, a and aborts. b) ---------------------------#
    # Toggles frame 3 between Readouts and Aborts
    def switch_3(self, desired_display):

        if desired_display == 'readouts':
            self.init_readouts()

        elif desired_display == 'aborts':
            self.init_aborts()

    ##########################################################################
    # --------- GUI functionality, setup widgets functions ------------------#
    # ---------- here see below section to add/subtract widgets --------------#
    ##########################################################################

    # --------------------------- Setup Aborts panel --------------------------- #
    def init_aborts(self):
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

    # --------------------------- Setup Readouts panel --------------------------- #
    def init_readouts(self):
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

    # --------------------------- Setup Manual panel --------------------------- #
    def init_manual(self):
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
        self.NC_IO = tk.Button(self.f2, text="NCIO", font=(font, 20), bg='#FF0000', fg='#FFFFFF', borderwidth=10,
                               relief='ridge', command=lambda: self.manual_sol_actuate("NCIO"))
        self.NC_IO.grid(column=8, row=2, sticky=(N, S, E, W))

        self.NC_IF = tk.Button(self.f2, text="NCIF", font=(font, 20), bg='#FF0000', fg='#FFFFFF', borderwidth=10,
                               relief='ridge')
        self.NC_IF.configure(command=lambda: self.manual_sol_actuate("NCIF"))
        self.NC_IF.grid(column=0, row=2, sticky=(N, S, E, W))

        self.NO_IP = tk.Button(self.f2, text="NOIP", font=(font, 20), bg='#FF0000', fg='#FFFFFF', borderwidth=10,
                               relief='ridge', command=lambda: self.manual_sol_actuate("NOIP"))
        self.NO_IP.grid(column=3, row=2, sticky=(N, S, E, W))

        self.NC_IP = tk.Button(self.f2, text="NCIP", font=(font, 20), bg='#FF0000', fg='#FFFFFF', borderwidth=10,
                               relief='ridge', command=lambda: self.manual_sol_actuate("NCIP"))
        self.NC_IP.grid(column=5, row=2, sticky=(N, S, E, W))

        self.NC_3O = tk.Button(self.f2, text="NC3O", font=(font, 20), bg='#FF0000', fg='#FFFFFF', borderwidth=10,
                               relief='ridge', command=lambda: self.manual_sol_actuate("NC3O"))
        self.NC_3O.grid(column=1, row=0, sticky=(N, S, E, W), padx=40, pady=40)

        self.NC_3N = tk.Button(self.f2, text="NC3N", font=(font, 20), bg='#FF0000', fg='#FFFFFF', borderwidth=10,
                               relief='ridge', command=lambda: self.manual_sol_actuate("NC3N"))
        self.NC_3N.grid(column=7, row=0, sticky=(N, S, E, W), padx=40, pady=40)

        self.NC_OP = tk.Button(self.f2, text="NCOP", font=(font, 20), bg='#FF0000', fg='#FFFFFF', borderwidth=10,
                               relief='ridge', command=lambda: self.manual_sol_actuate("NCOP"))
        self.NC_OP.grid(column=4, row=0, sticky=(N, S, E, W), padx=40, pady=40)

        self.arm_valves = tk.Button(self.f2, text="ARM Valves", font=(font, 15), bg='#ff7300', fg='#FFFFFF',
                                    borderwidth=20, relief='raised', command=self.enable_all)
        self.arm_valves.grid(column=4, row=1, sticky=(N, S, E, W), padx=40, pady=40)

        self.all_manual_btns = [self.NC_IO, self.NC_IF, self.NO_IP, self.NC_IP,
                                self.NC_3O, self.NC_3N, self.NC_OP]
        self.disable_all()

    # --------------------------- Manual Panel Logic Functions --------------------------- #

    # Enable all solenoids when ARM VALVES is pressed
    def enable_all(self):
        for btn in self.all_manual_btns:
            btn["state"] = "normal"

    # Disable all solenoids when ARM VALVES is pressed
    def disable_all(self):
        for btn in self.all_manual_btns:
            btn["state"] = "disabled"

    # Manually actuating a solenoid after valves ARMED
    def manual_sol_actuate(self, sol_name):
        self.SolManager.change_valve_state(sol_name)
        self.disable_all()

    # # this function actuates solenoids and changes button color based on previous state
    # def solenoid(self, solbutton):
    #     if arm == 1:
    #         if solbutton.cget('bg') == '#FF0000':
    #             GPIO.output(17, GPIO.HIGH)
    #             solbutton.configure(bg='#00FF00', relief='ridge')
    #             print(GPIO.input(10))
    #         elif solbutton.cget('bg') == '#00FF00':
    #             GPIO.output(17, GPIO.LOW)
    #             solbutton.configure(bg='#FF0000', relief='ridge')
    #             print(GPIO.input(10))
    #     elif arm == 0:
    #         return

    # --------------------------- Setup Fire panel --------------------------- #

    def init_fire(self):
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

        # place labels describing each of the toggles
        self.fire_ops = tk.Label(self.f1, text="Firing Mode", font=(font, 35, 'bold'), bg='#000000', fg='#FFFFFF')
        self.fire_ops.grid(column=1, row='0', sticky=(N, S, W, E))

        self.prefire_1 = tk.Label(self.f2, text="Valves in correct states", font=(font, 15), bg='#000000', fg='#FFFFFF')
        self.prefire_1.grid(column=4, row=2, sticky=(N, S, E, W))

        self.prefire_2 = tk.Label(self.f2, text="Sensor readings nominal", bg='#000000', font=(font, 15), fg='#FFFFFF')
        self.prefire_2.grid(column=4, row=3, sticky=(N, S, E, W))

        self.prefire_3 = tk.Label(self.f2, text="Range admin notified", bg='#000000', font=(font, 15), fg='#FFFFFF')
        self.prefire_3.grid(column=4, row=4, sticky=(N, S, E, W))

        self.prefire_4 = tk.Label(self.f2, text="Range is clear", bg='#000000', font=(font, 15), fg='#FFFFFF')
        self.prefire_4.grid(column=4, row=5, sticky=(N, S, E, W))

        self.prefire_5 = tk.Label(self.f2, text="Go/No go", bg='#000000', font=(font, 15), fg='#FFFFFF')
        self.prefire_5.grid(column=4, row=6, sticky=(N, S, E, W))

        self.prefire_6 = tk.Label(self.f2, text="Send it", bg='#000000', font=(font, 15), fg='#FFFFFF')
        self.prefire_6.grid(column=4, row=7, sticky=(N, S, E, W))

        # Place the toggles themselves
        self.toggle_1 = tk.Button(self.f2, bg='#000000', activebackground="#000000", image=self.toggle_off, height=60,
                                  width=135, highlightthickness=0, bd=0, command=lambda: self.prefire_toggle(self.toggle_1, "toggle_1"))
        self.toggle_1.grid(column=5, row=2, sticky=(N, S, E, W))

        self.toggle_2 = tk.Button(self.f2, bg='#000000', activebackground="#000000", image=self.toggle_off, height=60,
                                  width=135, highlightthickness=0, bd=0, command=lambda: self.prefire_toggle(self.toggle_2, "toggle_2"))
        self.toggle_2.grid(column=5, row=3, sticky=(N, S, E, W))

        self.toggle_3 = tk.Button(self.f2, bg='#000000', activebackground="#000000", image=self.toggle_off, height=60,
                                  width=135, highlightthickness=0, bd=0, command=lambda: self.prefire_toggle(self.toggle_3, "toggle_3"))
        self.toggle_3.grid(column=5, row=4, sticky=(N, S, E, W))

        self.toggle_4 = tk.Button(self.f2, bg='#000000', activebackground="#000000", image=self.toggle_off, height=60,
                                  width=135, highlightthickness=0, bd=0, command=lambda: self.prefire_toggle(self.toggle_4, "toggle_4"))
        self.toggle_4.grid(column=5, row=5, sticky=(N, S, E, W))

        self.toggle_5 = tk.Button(self.f2, bg='#000000', activebackground="#000000", image=self.toggle_off, height=60,
                                  width=135, highlightthickness=0, bd=0, command=lambda: self.prefire_toggle(self.toggle_5, "toggle_5"))
        self.toggle_5.grid(column=5, row=6, sticky=(N, S, E, W))

        self.toggle_6 = tk.Button(self.f2, bg='#000000', activebackground="#000000", image=self.toggle_off, height=60,
                                  width=135, highlightthickness=0, bd=0, command=lambda: self.prefire_toggle(self.toggle_6, "toggle_6"))
        self.toggle_6.grid(column=5, row=7, sticky=(N, S, E, W))

        self.abort_butt = tk.Button(self.f2, text="ABORT", font=(font, 18), bg='#FF0000', fg='#FFFFFF')
        self.abort_butt.grid(column=7, row=3, columnspan=1, rowspan=2, sticky=(N, S, E, W))

        self.fire_butt = tk.Button(self.f2, text="FIRE", font=(font, 20), bg='#ff7300', fg='#FFFFFF')
        self.fire_butt.grid(column=1, row=3, columnspan=1, rowspan=2, sticky=(N, S, E, W))

        # Relate names to objects
        self.toggle_dict = {"toggle_1": self.toggle_1,
                           "toggle_2": self.toggle_2,
                           "toggle_3": self.toggle_3,
                           "toggle_4": self.toggle_4,
                           "toggle_5": self.toggle_5,
                           "toggle_6": self.toggle_6,
                           "fire": self.fire_butt}
        # Set the toggles to whatever is stored in self.toggle_states
        self.set_toggles(self.toggle_dict)

    # --------------------------- Fire Panel Logic Functions --------------------------- #

    # Loops through dictionary
    def set_toggles(self, toggle_dict):
        for toggle_name in self.toggle_states:
            # print(toggle_name, self.toggle_states[toggle_name])
            
            # Enables/Disables toggle
            if self.toggle_states[toggle_name][0] is True:
                toggle_dict[toggle_name]["state"] = "normal"
            else:
                toggle_dict[toggle_name]["state"] = "disabled"
            
            # Sets toggle image to on/off
            if toggle_name is "fire":
                pass
            elif self.toggle_states[toggle_name][1] is True:
                toggle_dict[toggle_name].configure(image=self.toggle_on)
            else:
                toggle_dict[toggle_name].configure(image=self.toggle_off)


    # manual switch function
    # Prefire toggle
    def prefire_toggle(self, toggle, name):
        bck = str(toggle.cget('image'))
        # Transition from off -> on
        if bck == "pyimage1":
            # Set curr toggle to ON
            self.toggle_states[name][1] = True
            toggle.configure(image=self.toggle_on)

            # Enable next toggle
            next_tog_name = self.next_toggle[name]
            self.toggle_states[next_tog_name][0] = True
            self.toggle_dict[next_tog_name]["state"] = "normal"

        # Transition from on -> off
        else:
            # Set curr toggle to OFF
            self.toggle_states[name][1] = False
            toggle.configure(image=self.toggle_off)

            # Need to disable all the bottons after curr toggle in sequence
            next_tog_name = self.next_toggle[name]
            # Body executes until we reach a disabled button
            while self.toggle_states[next_tog_name][0] is True:

                # Disable next toggle
                self.toggle_states[next_tog_name][0] = False
                self.toggle_dict[next_tog_name]["state"] = "disabled"

                # Change photo of next toggle
                if next_tog_name is not "fire":
                    self.toggle_states[next_tog_name][1] = False
                    self.toggle_dict[next_tog_name].configure(image=self.toggle_off)

                # Get next toggle to check
                if next_tog_name is not "fire":
                    next_tog_name = self.next_toggle[next_tog_name]


########################################################################################################################
# -------------------------------------------------- THE END ----------------------------------------------------------#
########################################################################################################################
root = Tk()
my_gui = PrometheusGUI(root)
root.mainloop()