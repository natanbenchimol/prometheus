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

#### Design Principles:
During development there were a list of system requirements that were followed as well as a series of design principles
that had to be adhered to:

1. __Flexibility__ - This system needs to be able to support many different sensor configurations, firing sequences,
and igniters.
2. __Simplicity__ - We plan on _Prometheus_ having a long and successful life in the lab, this means that the system 
should be as intuitive as possible and incredibly well documented/commented so that lab members 3 years from now can 
configure it for their needs.
3. __Replicability__ - Need to be able to support multiple firings/tests in a short period, keep system setup and reset
as fast as possible.

#### Priorities:
During development we kept a few priorities of the system in mind when developing.
1. __Data Safety__ - Keeping data safe is the single most important priority. Data is how we measure success, 
troubleshoot issues, and write papers. At every point in development we must ensure that we find all potential failures
and account for them. 
2. __Maximize data collection frequency__ - Code should be efficient so that we can push the data collection frequencies
as high as possible. More data = better!


#### System Requirements:
* __GUI__ - Entire system must be controllable with a well designed user interface. 
* __Control System__ - Have complete control over all procedures and actuations during manual and firing operations 
* __Abort Handling__ - The system must check for and successfully handle aborts utilizing the concept of abort gates.
* __Data Acquisition__ - Record all the data produced by the firing. 
* __Data Processing__ - Crunch and process all of the data immediately following the firing, need to ensure data safety
by adding redundancies and adding security measures.
* __Data Visualizations__ - Produce graphs of system state over time immediately after firing.

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
   - Remove bloatware on your Pi, we don't need stuff like the wolfram engine taking up space, delete it. 
   [Guide here.](https://github.com/raspberrycoulis/remove-bloat)
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

__Note__ that this program generates a directory called `prometheus/Data` which will contain all of the data produced during any firing,
and a file called `prometheus/config.txt` that will hold the values for configuring the abort gates.
  
### Code Style Guide
The style convention chosen for this project can be confusing but we have tried to adhere to the following: 
- **ALL_CAPS** is used to denote global constants that can't be changed by the user once the GUI is running.
- **Capital_Case_With_Underscores** is used for shared structures that are read/modified by multiple files.
- **all_lower_case** is used for local vars
- **CapitalCaseNoSpaces** is used to denote custom structures/classes that we have built. 


## Detailed System Description
This section of the README will discuss the details of each of the modules that make up the system.

#### Control Systems

#### Abort Handling

#### Fire Sequence Loading
The code which takes the timings in from the front end and and creates a structure which can be understood by the solenoid 
manager class can be found in "prometheus_shared.py" in the function called `load_timings()` is unfortunately one of the most
complex pieces of code in the entire project.

The front end provides the back end with the start and end times for each of the firing actions relative to the 
countdown start, each of the firing actions are represented in the code with a solenoid actuation. The `load_timings()`
function takes in the inputs, transforms them into a data structure which can be interpreted by the sol manager. 
Additionally, for each firing action we need to calculate the time until the next action so we know how long we need the
system to sleep for.

#### Data Acquisition
All of the data acquisition for _Prometheus_ is handled inside the 'prometheus_daq.py' file. Here's a brief explanation
of how it works. First we should understand that the user will not have been able to fire the system without having gone
through a standardized firing procedure, with each step of the procedure represented by a switch on the GUI, we will not
be able to fire without flipping all the switches. Once the firing begins we create three instances of threads containing
the `batch_reader` function, one for each PTs/TCs/FMs. Each of these threads produce an instance of an instrument reader
thread, (either `readPT`, `readTC`, or `readFM`) for each sensor of that type in batches. These data points are then
checked against the abort gates, appended to their respective data lists and sent to the GUI via `LIVE_DICT`.

Note that the DAQ process is very independent from the firing procedure, the `batch_reader` threads continue to take data
readings until the `prom_status` dictionary tells it to stop. This means we can force the system to start recording when
the `fire()` function is called and then continue recording until after the fire + purge have both run to completion. 
This independence is very important to ensuring that we never fire without recording data.

#### Data Processing
The data processing for the system initiates immediately after the `batch_reader` threads finish and is entirely encapsulated
in the `write_to_file` function. The functions first action is to write all of the raw data to main memory, the processing
is quite CPU intensive since there is a lot of arithmetic going on. To avoid crashes that may happen during this dangerous
process we save all our data immediately and can come back to it later.

Next we need to format our data, I won't lie this is kinda complicated, sorry about that. I'll talk about all that we need
  to do to the data before we save it again, here's what the data looks like for reference:
> [batch_num, timestamp, instrument_name, reading]

For each batch of readings we need to find the average time of reading (the individual batch times will be different due
to how multi-threading works), then we need to take all the readings of the same batch number and collect them in one array
so that we can map each instrument to an average time, we also need to turn our timestamp into mission time and 24h time. Spend some time looking at the code and the two file formats and it
will make more sense.

#### Logfile
The logfile is a relatively simple system which records system parameters, system settings, and logs every event that occurs 
 during the firing. The logfile system is important for post-processing and examining the events of a firing. 

In order to log an event simply write:

`shared.log_event("<EVENT TYPE ACRONYM>", "<EVENT DESCRIPTION>")`

This function adds these events to a global array which gets written to 'logfile.txt' immediately after the firing has completed. 

## README TODO:
- How to add an instrument
- How to add solenoid
- Overall system explanation
- How to change daq
