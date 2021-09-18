# Hydriot IoT Node
This software serves as an example IoT node design for the Hydriot automation systems. This could be used in isolation and can be modified in any way deemed fit for your hydroponics needs, the intention is to make it easier for people to enter and customize their urban farming systems.

THe goal is to start Urban experimentation buy late 2021, this is a self-funded project so progres is slow but steady.

<img src="https://raw.githubusercontent.com/Hydriot/IoT-Node/main/resources/hydroponics_project.jpg" width="400" alt="Hydriot IoT Node Project"> <br/>

**What does this do?**
The idea is that you will build a IoT system that will
- [ ] Automate the hours of daylight from your grow lights connected directly from wall power
- [x] Run a 12v waterpump from battery (power failure) and cut the power if water in tank runs out
- [x] Monitor pH, TDS, water level, Co2, battery voltage, Temperature and Humidity
- [x] Programatically dose nutrients into the water reservoir
- [x] Programatically reduce pH from tap water
- [ ] Connect to cloud software that allows remote monitoring 

## Conceptual Architecture

<img src="https://raw.githubusercontent.com/Hydriot/IoT-Node/main/resources/Master%20Node.jpg" width="600" alt="Hydriot IoT Node Conseptual Architecture"> <br/>
The above design explains the high level components and how they are to be connected.

Refer to the Wiki page to help you set the project up yourself.


## Setup Guide
* [Hardware Setup](https://github.com/Hydriot/IoT-Node/wiki/Hardware-Setup)
* [Software Setup](https://github.com/Hydriot/IoT-Node/wiki/Software-Setup)

## Running Hydriot
After doing the hardware and software setup you can either run hydriot node from the Raspberri Pi or remotely.

### Run from Raspberri Pi
* If booted into terminal you could start GUI with "startx"
* Open VS Code (Can start from terminal using "code")
* Open "/home/pi/hydriot/IoT-Node" folder
* Run main.py

### Run Remotely
Ensure you have done the [remote configuration in the Wiki page](https://github.com/Hydriot/IoT-Node/wiki/Remote-SSH-Development-Setup). You are redirecting the display app so neeed to host a xserver locally.
* Open the remote location Pi > "/home/pi/hydriot/IoT-Node"
* Press Cntr+D (Special run configuration that points to loal pc as destination display)
* Run from debug


