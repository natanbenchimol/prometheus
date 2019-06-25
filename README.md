#Prometheus | Liquid Propulsion Lab | USC
##High Level Description

Prometheus is LPL's first feed-system based igniter for our rocket engines. 
The goal of this project is to design a Control & Data Acquisition Unit that will handle running a GUI, controlling sensors and other hardware, processing & saving information, and checking for & implementing abort scenarios if necessary.
Currently, we are using a Raspberry Pi 3B as our microcontroller and building the system in Python.
prometheus_gui_test.py runs the thread which handles the GUI and all of the associated functionality.
accessories directory contains images, objects, and other accessories that are called in our system.
    
###File Structure:
The 'Assets' directory contains all the images used in the GUI.
The 'Other' directory contains code snippets for syntax testing and old depreciated code.
All files inside the main directory are used in the running of the program.
Note that this program generates a directory called 'Data' which will contain all of the data produced during any firing.

###Contributers:

- **Sean Lissner** - USC B.S. Computer Science, May 2020
- **John Rogers** -  USC B.S. Astronautical Engineering, December 2021
- **Natan Benchimol** -  USC B.S. Electrical Engineering, December 2020

###IMPORTANT OPERATIONAL NOTES:
  - Python version: python3
  - required python packages: tkinter, PIL
  - Intended operational screen size is **** 20.5in (520.7mm) (Length) x 11.5in (292.1mm) (Height)****. If you are editing/testing the file on a smaller screen size, some adjustments may need to be made. These are mostly just visual adjustments and will most likely not affect functionality of the program. We intend to include notes at the top of prometheus_gui_test.py with instructions on what needs to be changed in order to factor in the adjusted screen size

#### README TODO:
- How to add an instrument
- How to add solenoid
- Overall system explanation
- How to change daq
