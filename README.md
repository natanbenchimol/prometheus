# Prometheus Test Stand | USC Liquid Propulsion Lab

## Contributors
- **Sean Lissner | Software Lead** - USC B.S. Computer Science, May 2020, | +1 (213) 458-1512 | slissner@usc.edu
- **Atticus Vadera | Project Manager** - USC PDP Astronautical Engineering
- **Natan Benchimol | Hardware Lead** -  USC B.S. Electrical Engineering, December 2020
- **John Rogers** -  USC B.S. Astronautical Engineering, December 2021

## High Level Description
_Prometheus_ is LPL's first igniter test stand for feed-based systems. As the lab grows and we begin to increase the power 
of our engines, the demand grows for more powerful ignition systems and more sophisticated testing hardware and methods 
for iterating on these systems. This repository contains the control systems for _Prometheus_ as well as its data acquisition
and data processing software.

During development there were a list of system requirements that were followed as well as a series of design principles
that had to be adhered to:

#### Design Principles:
1. __Flexibility__ - This system needs to be able to support many different sensor configurations, firing sequences,
and igniters.
2. __Simplicity__ - We plan on _Prometheus_ having a long and successful life in the lab, this means that the system 
should be as intuitive as possible and incredibly well documented/commented so that lab members 3 years from now can 
configure it for their needs.
3. __Replicability__ - Need to be able to support multiple firings/tests in a short period, keep system setup and reset
as fast as possible.

#### System Requirements:
* __GUI__ - Entire system must be controllable with a well designed user interface. 
* __Control System__ - Have complete control over all procedures and actuations during manual and firing operations 
* __Abort Handling__ - The system must check for and successfully handle aborts utilizing the concept of abort gates.
* __Data Acquisition__ - Record all the data produced by the firing. 
* __Data Processing__ - Crunch and process all of the data immediately following the firing, need to ensure data safety
by adding redundancies and adding security measures.
* __Data Visualization (Future)__ - Produce graphs of system state over time immediately after firing.

## Technical Specifications
#### Hardware:
This project was developed on a Raspberry Pi 3b with 1GB of RAM and a 1.5 GHz quad-core processor, any device with these
specs or better should perform just fine. It was designed for a screen with dimensions 20.5inches x 11.5inches but 
should auto-scale comfortably for most modern screens. For hardware add ons it is beneficial to equip your Pi with:
- A stable power supply (reduces number of random crashes)
- A CPU fan (aids overclocking)
- A good SD card (speeds up data processing time and adds a level of data safety)

#### Software:
The entire codebase is written in Python3 and uses the following external libraries that need to be installed on your
Raspberry Pi with pip or homebrew before it can run correctly:
- __tkinter__ - Python's standard GUI library, nice and flexible with lots of documentation online.
- __PIL__ - 
- __GPIO__ - Used for solenoid actuation.

#### Setup Instructions:
1. __Prepare the Pi__ - Before we even clone this repository it is best to setup your hardware so as to improve
 performance.
   - Install Python3 and the libraries listed above, all of the other libraries we use should be included in the
   installation of Python3.
   - Remove bloatware on your Pi, we don't need stuff like the wolfram engine taking up space, delete it. Guide here.
   - Configure system for overclocking, important to have a stable power supply and CPU fan if you intend to do this. Guide 
   here.
   - Add a system monitoring widget called Conky, tells you state of the Pi during the firing so you can look for
    anomalies. [Guide here.](https://www.novaspirit.com/2017/02/23/desktop-widget-raspberry-pi-using-conky/)
2. __Clone this repository__ - Pretty self explanatory, clone the codebase to your Pi.
3. __Configure your Codebase (TODO)__ - Super quick
   - Pin mappings
   - Generate a config file by running script in 'prometheus_shared.py'
   - Set firing sequence
    
### File Structure:
The 'Assets' directory contains all the images used in the GUI.
The 'Other' directory contains code snippets for syntax testing and old depreciated code.
All files inside the main directory are used in the running of the program.
Note that this program generates a directory called 'Data' which will contain all of the data produced during any firing.
  
### Code Style Guide
The style convention chosen for this project can be confusing but we have tried to adhere to the following: 
- **ALL_CAPS** is used to denote global constants that can't be changed by the user once the GUI is running.
- **Capital_Case_With_Underscores** is used for shared structures that are read/modified by multiple files.
- **all_lower_case** is used for local vars
- **CapitalCaseNoSpaces** is used to denote custom structures/classes that we have built. 


## Detailed System Description
This section of the README will discuss the details of each of the modules that make up the system.

#### Control System

#### Abort Handling

#### Data Acquisition
All of the data acquisition for _Prometheus_ is handled inside the 'prometheus_daq.py' file. Here's a brief explanation
of how it works. First we should understand that the user will not have been able to fire the system without having gone
through a standardized firing procedure, with each step of the procedure represented by a switch on the GUI, we will not
be able to fire without flipping all the switches. Once the firing begins we create three instances of threads containing
the `batch_reader` function, one for each PTs/TCs/FMs. Each of these threads produce an instance of an instrument reader
thread, either `readPT`, `readTC`, or `readFM`. 

#### Data Processing


## README TODO:
- How to add an instrument
- How to add solenoid
- Overall system explanation
- How to change daq