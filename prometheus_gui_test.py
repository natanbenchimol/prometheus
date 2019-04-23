import tkinter as tk
from tkinter import font
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

frame_setting = "MANUAL"      # "MANUAL"=manual ops, "FIRE"=fire ops



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

# test function for text in entry
def fs_focusin(event, entry):
    if (entry.get()=='Start' or entry.get()=='End' or entry.get()=='[seconds]' or entry.get()=='[Hz]'):
        entry.delete(0, 'end')
        entry.insert(0,'')
        entry.config(fg='black')

def fs_focusout0(event, entry, check):
    print(entry)
    if (entry.get()==''):
        if (check == "fire_duration"):
            entry.insert(0,"[seconds]")
        elif (check=="spark_freq"):
            entry.insert(0,"[Hz]")

        entry.config(fg='#5c5c8a', font=('Courier', 10, 'italic', 'bold'))

def fs_focusout1(event, entry):
    if(entry.get()==''):
        entry.insert(0,"Start")
        entry.config(fg='green', font=('Courier',10,'italic'))


def fs_focusout2(event, entry):
    if (entry.get()==''):
        entry.insert(0,'End')
        entry.config(fg='red', font=('Courier', 10, 'italic'))

def switch_frame(OPS, f_setting):
    global frame_setting
    #global OPS
    OPS = OPS.get()
    print("Start")
    print(OPS)
    if (f_setting=="FIRE" and OPS=="MANUAL"):
        frame1.tkraise()
        frame_setting = "MANUAL"
        print('manual')
    elif(f_setting=="MANUAL" and OPS=="FIRE"):
        frame4.tkraise()
        frame_setting = "FIRE"
        print('fire')


# following functions control actuating the button presses (currently turns from red to green)
def actuate_NCIP():
    if (button_NCIP.cget('bg')=='red'):
            button_NCIP.configure(bg='green')
            button_NCIP.configure(activebackground = button_NCIP.cget('bg'))
    elif (button_NCIP.cget('bg')=='green'):
        button_NCIP.configure(bg='red')
        button_NCIP.configure(activebackground = button_NCIP.cget('bg'))

def actuate_NCIF():
    if (button_NCIF.cget('bg')=='red'):
            button_NCIF.configure(bg='green')
            button_NCIF.configure(activebackground = button_NCIF.cget('bg'))
    elif (button_NCIF.cget('bg')=='green'):
        button_NCIF.configure(bg='red')
        button_NCIF.configure(activebackground = button_NCIF.cget('bg'))
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

#NCIF_FLAG = 0
#def actuate_NCIF():
#    global NCIF_FLAG  


#NCIO_FLAG = 0
#def actuate_NCIO():
#    global NCIO_FLAG 


#NOIP_FLAG = 0
#def actuate_NOIP():
#    global NOIP_FLAG


#NCIFO_FLAG = 0
#def actuate_NCIFO():
#    global NCIFO_FLAG


#NCIOP_FLAG = 0
#def actuate_NCIOP():
#    global NCIOP_FLAG




#gpio.setmode(gpio.BCM)
#gpio.setup(solenoid_pin, gpio.OUT)

###################################################################################################
# Frame Layout 
###################################################################################################

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='black')
canvas.pack()

# blue (main) nw frame
frame1 = tk.Frame(root, bg='#0059b3')
frame1.place(relx=0, rely=0.1, relwidth=0.7, relheight=0.6)

# pink e frame
frame2 = tk.Frame(root, bg='#ff1a8c')
frame2.place(relx=0.7, rely=0, relwidth=0.3, relheight=1)

#yellow s framce
frame3 = tk.Frame(root, bg='#ffff4d')
frame3.place(relx=0, rely=0.7, relwidth=0.7, relheight=0.3)

# green (second) nw frame (underneath main frame)
frame4 = tk.Frame(root, bg='#33ff33')
frame4.place(relx=0, rely=0.1, relwidth=0.7, relheight=0.60)

# variable to storing OPS setting
OPS = tk.StringVar()

fr_switch_button1 = tk.Radiobutton(root, text="MANUAL OPS", font=('Courier', 15, 'bold'), bg='green', activebackground='green', variable=OPS, value="MANUAL", command=lambda: switch_frame(OPS, frame_setting)) 
fr_switch_button1.place(relwidth=0.3, relheight=0.1)

fr_switch_button2 = tk.Radiobutton(root, text="FIRE OPS", font=('Courier', 15, 'bold'), bg='red', activebackground='red', variable=OPS, value="FIRE", command=lambda: switch_frame(OPS, frame_setting)) 
fr_switch_button2.place(relx=0.4, relwidth=0.3, relheight=0.1)


frame1.tkraise()

###################################################################################################
# Manual Ops 
###################################################################################################

button_NCIP = tk.Button(frame1, text="NC-IP", font=('Courier', 20, 'bold'), bg='red',activebackground='red',  command=actuate_NCIP)
button_NCIP.place(relx=0.03, rely=0.333, relwidth=NC_BUTTONWIDTH, relheight=NC_BUTTONHEIGHT)

button_NCIF = tk.Button(frame1, text="NC-IF", font=('Courier', 20, 'bold'), bg='red', activebackground='red', command=actuate_NCIF)
button_NCIF.place(relx=0.3433, rely=0.333, relwidth=NC_BUTTONWIDTH, relheight=NC_BUTTONHEIGHT)

button_NCIO = tk.Button(frame1, text="NC-IO", font=('Courier', 20, 'bold'), bg='red',activebackground='red',  command=actuate_NCIO)
button_NCIO.place(relx=0.6566, rely=0.333, relwidth=NC_BUTTONWIDTH, relheight=NC_BUTTONHEIGHT)

button_NOIP = tk.Button(frame1, text="NO-IP", font=('Courier', 20, 'bold'), bg='red',activebackground='red',  command=actuate_NOIP)
button_NOIP.place(relx=0.03, rely=0.666, relwidth=NC_BUTTONWIDTH, relheight=NC_BUTTONHEIGHT)

button_NCIFO = tk.Button(frame1, text="NC-IFO", font=('Courier', 20, 'bold'), bg='red',activebackgroun='red', command=actuate_NCIFO)
button_NCIFO.place(relx=0.3433, rely=0.666, relwidth=NC_BUTTONWIDTH, relheight=NC_BUTTONHEIGHT)

button_NCIOP = tk.Button(frame1, text="NC-IOP", font=('Courier', 20, 'bold'), bg='red', activebackgroun='red', command=actuate_NCIOP)
button_NCIOP.place(relx=0.6566, rely=0.666, relwidth=NC_BUTTONWIDTH, relheight=NC_BUTTONHEIGHT)


###################################################################################################
# Firing Ops 
###################################################################################################




###################################################################################################
# Firing Sequence 
##################################################################################################


# Main labels
#------------
fire_duration_label = tk.Label(frame3, text="Fire Duration [s] ", font=(FS_FONT, '8', 'bold'), bg='black', fg='white')
fire_duration_label.place(relx=0.05, rely=0.15, relwidth=FS_WIDTH, relheight=FS_HEIGHT)

spark_timing_label = tk.Label(frame3, text="Spark Timing  [Hz]", font=(FS_FONT, '8', 'bold'), bg='black', fg='white')
spark_timing_label.place(relx=0.05, rely=0.32, relwidth=FS_WIDTH, relheight=FS_HEIGHT)

spark_freq_label = tk.Label(frame3, text="Spark Frequency", font=(FS_FONT, '8', 'bold'), bg='black', fg='white')
spark_freq_label.place(relx=0.05, rely=0.49, relwidth=FS_WIDTH, relheight=FS_HEIGHT)

NCIO_timing_label = tk.Label(frame3, text="NC - IO Timing", font=(FS_FONT, '9', 'bold'), bg='black', fg='white')
NCIO_timing_label.place(relx=0.05, rely=0.66, relwidth=FS_WIDTH, relheight=FS_HEIGHT)

NCIF_timing_label = tk.Label(frame3, text="NC - IF Timing", font=(FS_FONT, '9', 'bold'), bg='black', fg='white')
NCIF_timing_label.place(relx=0.05, rely=0.83, relwidth=FS_WIDTH, relheight=FS_HEIGHT)

# Inputs
#------------
fire_duration_entry = tk.Entry(frame3, bg='white', justify='center', fg='#5c5c8a', font=('Courier', 10, 'bold', 'italic'))
fire_duration_entry.place(relx=0.390, rely=0.150, relwidth=0.160, relheight=0.14)

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

















root.mainloop()
