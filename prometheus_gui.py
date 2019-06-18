import tkinter as tk
from tkinter import font
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
#import RPi.GPIO as gpio

# hexadecimal color scheme at www.w3schools.com/colors/colors_picker.asp

HEIGHT = 700
WIDTH = 800


solenoid_pin = 18
s_flag = 0

NC_BUTTONWIDTH = 0.2733
NC_BUTTONHEIGHT = 0.2

font = 'System'     # font declaration
FS_FONT = font
FS_WIDTH = 0.26
FS_HEIGHT = 0.14

frame_setting = "MANUAL"    # Initializes to "MANUAL"
                            # "MANUAL" = manual ops, "FIRE" = fire ops

# this function handles functionality of actuating a solenoid with gpio pins
# we used it for initial testing, and have left it here for syntax reference later on
def actuate_solenoid():
    global s_flag
    if (s_flag == 0):
        gpio.output(solenoid_pin, gpio.HIGH)    
        s_flag =1
        print("SOLENOID HAS BEEN opened")
    elif (s_flag == 1):
        gpio.output(solenoid_pin, gpio.LOW)
        s_flag = 0
        print("SOLENOID HAS BEEN closed")

# This function handles clearing all the Input fields and preparing them for user input
# Input boxes are the 8 fields located in the bottom frame
def fs_focusin(event, entry):
    if (entry.get()=='Start' or entry.get()=='End' or entry.get()=='[seconds]' or entry.get()=='[Hz]'):
        entry.delete(0, 'end')
        entry.insert(0,'')
        entry.config(fg='black')


# this function handles resetting the instructions in each of the entry/input fields when the user removes focus from them. Separate functions are needed for each type of field
# this function handles "fire duration" and "spark frequency" fields
# Input boxes are the 8 fields located in the bottom frame
def fs_focusout0(event, entry, check):
    print(entry)
    if (entry.get()==''):
        if (check == "fire_duration"):
            entry.insert(0,"[seconds]")
        elif (check=="spark_freq"):
            entry.insert(0,"[Hz]")

        entry.config(fg='#5c5c8a', font=('Courier', 10, 'italic', 'bold'))


# this function handles resetting the instructions in each of the entry/input fields when the user removes focus from them. Separate functions are needed for each type of field
# this function handles "Start" fields
# Input boxes are the 8 fields located in the bottom frame
def fs_focusout1(event, entry):
    if(entry.get()==''):
        entry.insert(0,"Start")
        entry.config(fg='green', font=('Courier',10,'italic'))


# this function handles resetting the instructions in each of the entry/input fields when the user removes focus from them. Separate functions are needed for each type of field
# this function handles "End" fields
# Input boxes are the 8 fields located in the bottom frame
def fs_focusout2(event, entry):
    if (entry.get()==''):
        entry.insert(0,'End')
        entry.config(fg='red', font=('Courier', 10, 'italic'))


# this function handles the control for switching frames. It is called when either of the frame switching buttons is pressed
# Note: frame_setting and OPS are both used in order to determine previous and current state of frame. This allows us to avoid uneccessary action
def switch_frame(OPS):
    global frame_setting
    OPS = OPS.get()
    if (frame_setting=="FIRE" and OPS=="MANUAL"):   # switches to Manual Ops frame
        frame1.tkraise()        # switches to Firing Ops by raising Manual Ops frame on top of Firing Ops frame
        frame_setting = "MANUAL"
        fire_ops_switch.config(bg='red', activebackground='red')
        manual_ops_switch.config(bg='green', activebackground='green')

    elif(frame_setting=="MANUAL" and OPS=="FIRE"):  # switches to Firing Ops frame
        frame4.tkraise()        # switches to Firing Ops by raising Firing Ops frame on top of Manual Ops frame
        frame_setting = "FIRE"
        fire_ops_switch.config(bg='green', activebackground='green')
        manual_ops_switch.config(bg='red', activebackground='red')


# the following functions control actuating the button presses (currently turns from red to green)
# currently, they just change color to indicate button press detection
def actuate_NCIP():
    if (button_NCIP.cget('bg')=='red'):
        button_NCIP.config(bg='green')
        button_NCIP.config(activebackground = button_NCIP.cget('bg'))
    elif (button_NCIP.cget('bg')=='green'):
        button_NCIP.config(bg='red')
        button_NCIP.config(activebackground = button_NCIP.cget('bg'))

def actuate_NCIF():
    if (button_NCIF.cget('bg')=='red'):
        button_NCIF.config(bg='green')
        button_NCIF.config(activebackground = button_NCIF.cget('bg'))
    elif (button_NCIF.cget('bg')=='green'):
        button_NCIF.config(bg='red')
        button_NCIF.config(activebackground = button_NCIF.cget('bg'))
    print("ncif")

def actuate_NCIO():
    if (button_NCIO.cget('bg')=='red'):
        button_NCIO.configure(bg='green')
        button_NCIO.configure(activebackground = button_NCIO.cget('bg'))
    elif (button_NCIO.cget('bg')=='green'):
        button_NCIO.configure(bg='red')
        button_NCIO.configure(activebackground = button_NCIO.cget('bg'))
        print("ncio")

def actuate_NOIP():
    if (button_NOIP.cget('bg')=='red'):
        button_NOIP.configure(bg='green')
        button_NOIP.configure(activebackground = button_NOIP.cget('bg'))
    elif (button_NOIP.cget('bg')=='green'):
        button_NOIP.configure(bg='red')
        button_NOIP.configure(activebackground = button_NOIP.cget('bg'))
    print("noip")

def actuate_NCIFO():
    if (button_NCIFO.cget('bg')=='red'):
        button_NCIFO.configure(bg='green')
        button_NCIFO.configure(activebackground = button_NCIFO.cget('bg'))
    elif (button_NCIFO.cget('bg')=='green'):
        button_NCIFO.configure(bg='red')
        button_NCIFO.configure(activebackground = button_NCIFO.cget('bg'))
    print("ncifo")

def actuate_NCIOP():
    if (button_NCIOP.cget('bg')=='red'):
        button_NCIOP.configure(bg='green')
        button_NCIOP.configure(activebackground = button_NCIOP.cget('bg'))
    elif (button_NCIOP.cget('bg')=='green'):
        button_NCIOP.configure(bg='red')
        button_NCIOP.configure(activebackground = button_NCIOP.cget('bg'))
    print("nciop")

# this functions enables/disables the manual operation buttons when the "arm valves" button is pressed
#
def arm_man_ops_func(arm_man_ops_val):
    if(arm_man_ops_val.get()==1):
       button_NCIP.config(state='normal')
       button_NCIF.config(state='normal')
       button_NCIO.config(state='normal')
       button_NOIP.config(state='normal')
       button_NCIFO.config(state='normal')
       button_NCIOP.config(state='normal')
       arm_man_ops.config(image=disarming_switch_render)    # switches image to toggled off state
       arm_man_ops.image = disarming_switch_render          # handles image rendering (necessary for changing images)
       print("buttons enabled")                             # for debugging
    else:
        button_NCIP.config(state='disabled')
        button_NCIF.config(state='disabled')
        button_NCIO.config(state='disabled')
        button_NOIP.config(state='disabled')
        button_NCIFO.config(state='disabled')
        button_NCIOP.config(state='disabled')
        arm_man_ops.config(image=arming_switch_render)      # switches image to toggled on state
        arm_man_ops.image = arming_switch_render            # handles image rendering (necessary for changing images)
        print("buttons disabled")                           # for debugging


# these 2 lines below are kept for setting up gpio later on:

#gpio.setmode(gpio.BCM)
#gpio.setup(solenoid_pin, gpio.OUT)

###################################################################################################
# General Frame Setup
###################################################################################################

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='black')
canvas.pack()

# blue (main) top frame blue = #0059b3
frame1 = tk.Frame(root, bg='#000033')
frame1.place(relx=0, rely=0.1, relwidth=0.7, relheight=0.6)

# pink right frame pink = #ff1a8c
frame2 = tk.Frame(root, bg='#000033')
frame2.place(relx=0.7, rely=0, relwidth=0.3, relheight=1)

#yellow bottom frame  yellow = #ffff4d
frame3 = tk.Frame(root, bg='#000033')
frame3.place(relx=0, rely=0.7, relwidth=0.7, relheight=0.3)

# green (second) top frame (underneath main frame) green = #33ff33
frame4 = tk.Frame(root, bg='#000033')
frame4.place(relx=0, rely=0.1, relwidth=0.7, relheight=0.60)

# inserts LPL Logo
logo_load = Image.open('Assets/logo.jpg').resize((100,65), Image.ANTIALIAS)    # resize values are experiementally determined based on screen size. Not sure what ANTIALIAS does, but it was in every online example
logo_render = ImageTk.PhotoImage(logo_load)
logo = tk.Label(root, image=logo_render)
logo.image = logo_render
logo.place(relx=0.25, relwidth=0.2)

#border1 = tk.create_line(400, 401, 0, 400)

###################################################################################################
# Frame Switching Mechanism
###################################################################################################
OPS = tk.StringVar()    # variable to storing OPS setting (either "MANUAL" or "FIRE", depending on the desired frame)

manual_ops_switch = tk.Radiobutton(root, text="MANUAL OPS", font=('System', 15, 'bold'), bg='green', activebackground='green', variable=OPS, value="MANUAL", command=lambda: switch_frame(OPS))
manual_ops_switch.place(relwidth=0.25, relheight=0.1)

fire_ops_switch = tk.Radiobutton(root, text="FIRE OPS", font=('System', 15, 'bold'), bg='red', activebackground='red', variable=OPS, value="FIRE", command=lambda: switch_frame(OPS))
fire_ops_switch.place(relx=0.45, relwidth=0.25, relheight=0.1)

frame1.tkraise()        # raises the Manual Ops frame upon startup

###################################################################################################
# Manual Ops Frame Layout
###################################################################################################

man_ops_label = tk.Label(frame1, text="Manual Operations", font=('System', 22, 'bold', 'underline'), bg='#000033', fg='white')
man_ops_label.place(relx=0.25, relwidth=0.5)

arm_man_ops_label = tk.Label(frame1, text="Arm/Disarm Valves", font=('System', 16, 'bold'), bg='#000033', fg='white')
arm_man_ops_label.place(rely=0.116)

button_NCIP = tk.Button(frame1, text="NC-IP", font=('Courier', 20, 'bold'), state='disabled', bg='red', activebackground='red', command=lambda: actuate_NCIP())
button_NCIP.place(relx=0.03, rely=0.4, relwidth=NC_BUTTONWIDTH, relheight=NC_BUTTONHEIGHT)

button_NCIF = tk.Button(frame1, text="NC-IF", font=('Courier', 20, 'bold'), state='disabled', bg='red', activebackground='red', command=lambda: actuate_NCIF())
button_NCIF.place(relx=0.3433, rely=0.4, relwidth=NC_BUTTONWIDTH, relheight=NC_BUTTONHEIGHT)

button_NCIO = tk.Button(frame1, text="NC-IO", font=('Courier', 20, 'bold'), state='disabled', bg='red',activebackground='red',  command=actuate_NCIO)
button_NCIO.place(relx=0.6566, rely=0.4, relwidth=NC_BUTTONWIDTH, relheight=NC_BUTTONHEIGHT)

button_NOIP = tk.Button(frame1, text="NO-IP", font=('Courier', 20, 'bold'), state='disabled', bg='red',activebackground='red',  command=actuate_NOIP)
button_NOIP.place(relx=0.03, rely=0.73, relwidth=NC_BUTTONWIDTH, relheight=NC_BUTTONHEIGHT)

button_NCIFO = tk.Button(frame1, text="NC-IFO", font=('Courier', 20, 'bold'), state='disabled', bg='red',activebackgroun='red', command=actuate_NCIFO)
button_NCIFO.place(relx=0.3433, rely=0.73, relwidth=NC_BUTTONWIDTH, relheight=NC_BUTTONHEIGHT)

button_NCIOP = tk.Button(frame1, text="NC-IOP", font=('Courier', 20, 'bold'), state='disabled', bg='red', activebackgroun='red', command=actuate_NCIOP)
button_NCIOP.place(relx=0.6566, rely=0.73, relwidth=NC_BUTTONWIDTH, relheight=NC_BUTTONHEIGHT)

# next 4 lines handle image loading for arm/disarm valves switch
# an image is loaded as the background instead of an actual switch
arming_switch_load = Image.open('Assets/toggle_off.png').resize((100, 100), Image.ANTIALIAS)
arming_switch_render = ImageTk.PhotoImage(arming_switch_load)
disarming_switch_load = Image.open('Assets/toggle_on.png').resize((100, 100), Image.ANTIALIAS)
disarming_switch_render = ImageTk.PhotoImage(disarming_switch_load)

arm_man_ops_val = tk.IntVar()
arm_man_ops = tk.Checkbutton(frame1, text="Arm Valves", image=arming_switch_render, bg='#000033', command=lambda: arm_man_ops_func(arm_man_ops_val), variable=arm_man_ops_val)
arm_man_ops.image = arming_switch_render
arm_man_ops.place(rely=0.18, relwidth=0.2, relheight=0.2)


###################################################################################################
# Firing Ops Frame Layout
###################################################################################################




##################################################################################################
# Firing Sequence 
##################################################################################################


# Main labels
#------------
firing_sequence_label = tk.Label(frame3, text='Firing Sequence', font=(FS_FONT, 17, 'bold', 'underline'), bg='#000033', fg='white')
firing_sequence_label.place(relx=0.36, rely=0, relwidth=FS_WIDTH+0.02, relheight=0.11)

fire_duration_label = tk.Label(frame3, text="Fire Duration [s] ", font=(FS_FONT, 10, 'bold'), bg='black', fg='white')
fire_duration_label.place(relx=0.05, rely=0.15, relwidth=FS_WIDTH, relheight=FS_HEIGHT)

spark_timing_label = tk.Label(frame3, text="Spark Timing  [Hz]", font=(FS_FONT, 10, 'bold'), bg='black', fg='white')
spark_timing_label.place(relx=0.05, rely=0.32, relwidth=FS_WIDTH, relheight=FS_HEIGHT)

spark_freq_label = tk.Label(frame3, text="Spark Frequency", font=(FS_FONT, 10, 'bold'), bg='black', fg='white')
spark_freq_label.place(relx=0.05, rely=0.49, relwidth=FS_WIDTH, relheight=FS_HEIGHT)

NCIO_timing_label = tk.Label(frame3, text="NC - IO Timing", font=(FS_FONT, 10, 'bold'), bg='black', fg='white')
NCIO_timing_label.place(relx=0.05, rely=0.66, relwidth=FS_WIDTH, relheight=FS_HEIGHT)

NCIF_timing_label = tk.Label(frame3, text="NC - IF Timing", font=(FS_FONT, 10, 'bold'), bg='black', fg='white')
NCIF_timing_label.place(relx=0.05, rely=0.83, relwidth=FS_WIDTH, relheight=FS_HEIGHT)

# Inputs
#------------
fire_duration_entry = tk.Entry(frame3, bg='white', justify='center', fg='#5c5c8a', font=('Courier', 10, 'bold', 'italic'))
fire_duration_entry.place(relx=0.390, rely=0.15, relwidth=0.160, relheight=0.14)

spark_freq_entry = tk.Entry(frame3, bg='white', justify='center', fg='#5c5c8a', font=('Courier', 10, 'bold', 'italic'))
spark_freq_entry.place(relx=0.390, rely=0.32, relwidth=0.160, relheight=0.14)

spark_timing_entry1 = tk.Entry(frame3, bg='white', justify='center', fg='green', font=('Courier',10,'italic', 'bold'))
spark_timing_entry1.place(relx=0.36, rely=0.49, relwidth=0.09, relheight=0.14)

spark_timing_entry2 = tk.Entry(frame3, bg='white', justify='center', fg='red', font=('Courier',10,'italic'))
spark_timing_entry2.place(relx=0.49, rely=0.49, relwidth=0.09, relheight=0.14)

NCIO_timing_entry1 = tk.Entry(frame3, bg='white', justify='center', fg='green', font=('Courier',10,'italic'))
NCIO_timing_entry1.place(relx=0.36, rely=0.66, relwidth=0.09, relheight=0.14)

NCIO_timing_entry2 = tk.Entry(frame3, bg='white', justify='center', fg='red', font=('Courier',10,'italic'))
NCIO_timing_entry2.place(relx=0.49, rely=0.66, relwidth=0.09, relheight=0.14)

NCIF_timing_entry1 = tk.Entry(frame3, bg='white', justify='center', fg='green', font=('Courier',10,'italic'))
NCIF_timing_entry1.place(relx=0.36, rely=0.83, relwidth=0.09, relheight=0.14)

NCIF_timing_entry2 = tk.Entry(frame3, bg='white', justify='center', fg='red', font=('Courier',10,'italic'))
NCIF_timing_entry2.place(relx=0.49, rely=0.83, relwidth=0.09, relheight=0.14)

fire_duration_entry.insert(0, "[seconds]")
fire_duration_entry.bind('<FocusIn>', lambda event: fs_focusin(1,fire_duration_entry))
fire_duration_entry.bind('<FocusOut>', lambda event: fs_focusout0(1,fire_duration_entry, "fire_duration"))

spark_freq_entry.insert(0, "[Hz]")
spark_freq_entry.bind('<FocusIn>', lambda event: fs_focusin(1,spark_freq_entry))
spark_freq_entry.bind('<FocusOut>', lambda event: fs_focusout0(1,spark_freq_entry, "spark_freq"))

spark_timing_entry1.insert(0, "Start")
spark_timing_entry1.bind('<FocusIn>', lambda event: fs_focusin(1,spark_timing_entry1))
spark_timing_entry1.bind('<FocusOut>', lambda event: fs_focusout1(1,spark_timing_entry1))

spark_timing_entry2.insert(0, "End")
spark_timing_entry2.bind('<FocusIn>', lambda event: fs_focusin(1,spark_timing_entry2))
spark_timing_entry2.bind('<FocusOut>', lambda event: fs_focusout2(1,spark_timing_entry2))

NCIO_timing_entry1.insert(0, "Start")
NCIO_timing_entry1.bind('<FocusIn>', lambda event: fs_focusin(1,NCIO_timing_entry1))
NCIO_timing_entry1.bind('<FocusOut>', lambda event: fs_focusout1(1,NCIO_timing_entry1))

NCIO_timing_entry2.insert(0, "End")
NCIO_timing_entry2.bind('<FocusIn>', lambda event: fs_focusin(1,NCIO_timing_entry2))
NCIO_timing_entry2.bind('<FocusOut>', lambda event: fs_focusout2(1,NCIO_timing_entry2))

NCIF_timing_entry1.insert(0, "Start")
NCIF_timing_entry1.bind('<FocusIn>', lambda event: fs_focusin(1,NCIF_timing_entry1))
NCIF_timing_entry1.bind('<FocusOut>', lambda event: fs_focusout1(1,NCIF_timing_entry1))

NCIF_timing_entry2.insert(0, "End")
NCIF_timing_entry2.bind('<FocusIn>', lambda event: fs_focusin(1,NCIF_timing_entry2))
NCIF_timing_entry2.bind('<FocusOut>', lambda event: fs_focusout2(1,NCIF_timing_entry2))

# Progress Bars
#--------------

fire_duration_bar = Progressbar(frame3, length=200)
fire_duration_bar.place(relx=0.62, rely=0.16, relwidth=0.36, relheight=0.12)

spark_freq_bar = Progressbar(frame3, length=200)
spark_freq_bar.place(relx=0.62, rely=0.33, relwidth=0.36, relheight=0.12)

spark_timing_bar = Progressbar(frame3, length=200)
spark_timing_bar.place(relx=0.62, rely=0.5, relwidth=0.36, relheight=0.12)

NCIO_timing_bar = Progressbar(frame3, length=200)
NCIO_timing_bar.place(relx=0.62, rely=0.67, relwidth=0.36, relheight=0.12)

NCIF_timing_bar = Progressbar(frame3, length=200)
NCIF_timing_bar.place(relx=0.62, rely=0.84, relwidth=0.36, relheight=0.12)



##################################################################################################
# Sensor Readouts and Warnings (srw)
##################################################################################################
# This frame displays the readouts from sensors and displays warning lights of sensors if necessary
# 8 PT's and 7 TC's
# PT1_IP_readout, PT2_IP_readout, PT1_IF_readout, PT2_IF_readout, PT_I_readout, PT1_IO_readout, PT2_IO_readout, PT3_IO_readout
# TC1_IP_readout, TC2_IP_readout, TC1_IF_readout, TC_I_readout, TC1_IO_readout, TC2_IO_readout, TC3_IO_readout

srw_label = tk.Label(frame2, text="Sensor Readouts \n& Warnings", bg='#000033', fg='white', justify='center', font=('System', 20, 'bold', 'underline'))
srw_label.place(relwidth=1, relheight=0.08)

PT1_IP_label = tk.Label(frame2, text="PT1-IP", bg='black', fg='white', justify='center', font=('Courier', 20, 'bold'))
PT1_IP_label.place(relx=0.01, rely=0.1, relheight=0.05, relwidth=0.38)
PT1_IP_readout = tk.Label(frame2, text="123456789", bg='white', fg='black', justify='center', font=('Courier', 23, 'bold'))
PT1_IP_readout.place(relx=0.4, rely=0.1, relheight=0.05, relwidth=0.3)

PT2_IP_label = tk.Label(frame2, text="PT2-IP", bg='black', fg='white', justify='center', font=('Courier', 20, 'bold'))
PT2_IP_label.place(relx=0.01, rely=0.16, relheight=0.05, relwidth=0.38)
PT2_IP_readout = tk.Label(frame2, text="0", bg='white', fg='black', justify='center', font=('Courier', 23, 'bold'))
PT2_IP_readout.place(relx=0.4, rely=0.16, relheight=0.05, relwidth=0.3)

PT1_IF_label = tk.Label(frame2, text="PT1-IF", bg='black', fg='white', justify='center', font=('Courier', 20, 'bold'))
PT1_IF_label.place(relx=0.01, rely=0.22, relheight=0.05, relwidth=0.38)
PT1_IF_readout = tk.Label(frame2, text="0", bg='white', fg='black', justify='center', font=('Courier', 23, 'bold'))
PT1_IF_readout.place(relx=0.4, rely=0.22, relheight=0.05, relwidth=0.3)

PT2_IF_label = tk.Label(frame2, text="PT2-IF", bg='black', fg='white', justify='center', font=('Courier', 20, 'bold'))
PT2_IF_label.place(relx=0.01, rely=0.28, relheight=0.05, relwidth=0.38)
PT2_IF_readout = tk.Label(frame2, text="0", bg='white', fg='black', justify='center', font=('Courier', 23, 'bold'))
PT2_IF_readout.place(relx=0.4, rely=0.28, relheight=0.05, relwidth=0.3)

PT_I_label = tk.Label(frame2, text="PT-I", bg='black', fg='white', justify='center', font=('Courier', 20, 'bold'))
PT_I_label.place(relx=0.01, rely=0.34, relheight=0.05, relwidth=0.38)
PT_I_readout = tk.Label(frame2, text="0", bg='white', fg='black', justify='center', font=('Courier', 23, 'bold'))
PT_I_readout.place(relx=0.4, rely=0.34, relheight=0.05, relwidth=0.3)

PT1_IO_label = tk.Label(frame2, text="PT1-IO", bg='black', fg='white', justify='center', font=('Courier', 20, 'bold'))
PT1_IO_label.place(relx=0.01, rely=0.4, relheight=0.05, relwidth=0.38)
PT1_IO_readout = tk.Label(frame2, text="0", bg='white', fg='black', justify='center', font=('Courier', 23, 'bold'))
PT1_IO_readout.place(relx=0.4, rely=0.4, relheight=0.05, relwidth=0.3)

PT2_IO_label = tk.Label(frame2, text="PT2-IO", bg='black', fg='white', justify='center', font=('Courier', 20, 'bold'))
PT2_IO_label.place(relx=0.01, rely=0.46, relheight=0.05, relwidth=0.38)
PT2_IO_readout = tk.Label(frame2, text="0", bg='white', fg='black', justify='center', font=('Courier', 23, 'bold'))
PT2_IO_readout.place(relx=0.4, rely=0.46, relheight=0.05, relwidth=0.3)

PT3_IO_label = tk.Label(frame2, text="PT3-IO", bg='black', fg='white', justify='center', font=('Courier', 20, 'bold'))
PT3_IO_label.place(relx=0.01, rely=0.52, relheight=0.05, relwidth=0.38)
PT3_IO_readout = tk.Label(frame2, text="0", bg='white', fg='black', justify='center', font=('Courier', 23, 'bold'))
PT3_IO_readout.place(relx=0.4, rely=0.52, relheight=0.05, relwidth=0.3)

# TC1_IP_readout, TC2_IP_readout, TC1_IF_readout, TC_I_readout, TC1_IO_readout, TC2_IO_readout, TC3_IO_readout

TC1_IP_label = tk.Label(frame2, text="TC1-IP", bg='black', fg='white', justify='center', font=('Courier', 20, 'bold'))
TC1_IP_label.place(relx=0.01, rely=0.58, relheight=0.05, relwidth=0.38)
TC1_IP_readout = tk.Label(frame2, text="0", bg='white', fg='black', justify='center', font=('Courier', 23, 'bold'))
TC1_IP_readout.place(relx=0.4, rely=0.58, relheight=0.05, relwidth=0.3)

TC2_IP_label = tk.Label(frame2, text="TC2-IP", bg='black', fg='white', justify='center', font=('Courier', 20, 'bold'))
TC2_IP_label.place(relx=0.01, rely=0.64, relheight=0.05, relwidth=0.38)
TC2_IP_readout = tk.Label(frame2, text="0", bg='white', fg='black', justify='center', font=('Courier', 23, 'bold'))
TC2_IP_readout.place(relx=0.4, rely=0.64, relheight=0.05, relwidth=0.3)

TC1_IF_label = tk.Label(frame2, text="TC1-IF", bg='black', fg='white', justify='center', font=('Courier', 20, 'bold'))
TC1_IF_label.place(relx=0.01, rely=0.7, relheight=0.05, relwidth=0.38)
TC1_IF_readout = tk.Label(frame2, text="0", bg='white', fg='black', justify='center', font=('Courier', 23, 'bold'))
TC1_IF_readout.place(relx=0.4, rely=0.7, relheight=0.05, relwidth=0.3)

TC_I_label = tk.Label(frame2, text="TC-I", bg='black', fg='white', justify='center', font=('Courier', 20, 'bold'))
TC_I_label.place(relx=0.01, rely=0.76, relheight=0.05, relwidth=0.38)
TC_I_readout = tk.Label(frame2, text="0", bg='white', fg='black', justify='center', font=('Courier', 23, 'bold'))
TC_I_readout.place(relx=0.4, rely=0.76, relheight=0.05, relwidth=0.3)

TC1_IO_label = tk.Label(frame2, text="TC1-IO", bg='black', fg='white', justify='center', font=('Courier', 20, 'bold'))
TC1_IO_label.place(relx=0.01, rely=0.82, relheight=0.05, relwidth=0.38)
TC1_IO_readout = tk.Label(frame2, text="0", bg='white', fg='black', justify='center', font=('Courier', 23, 'bold'))
TC1_IO_readout.place(relx=0.4, rely=0.82, relheight=0.05, relwidth=0.3)

TC2_IO_label = tk.Label(frame2, text="TC2-IO", bg='black', fg='white', justify='center', font=('Courier', 20, 'bold'))
TC2_IO_label.place(relx=0.01, rely=0.88, relheight=0.05, relwidth=0.38)
TC2_IO_readout = tk.Label(frame2, text="0", bg='white', fg='black', justify='center', font=('Courier', 23, 'bold'))
TC2_IO_readout.place(relx=0.4, rely=0.88, relheight=0.05, relwidth=0.3)

TC3_IO_label = tk.Label(frame2, text="TC3-IO", bg='black', fg='white', justify='center', font=('Courier', 20, 'bold'))
TC3_IO_label.place(relx=0.01, rely=0.94, relheight=0.05, relwidth=0.38)
TC3_IO_readout = tk.Label(frame2, text="0", bg='white', fg='black', justify='center', font=('Courier', 23, 'bold'))
TC3_IO_readout.place(relx=0.4, rely=0.94, relheight=0.05, relwidth=0.3)



root.mainloop()
