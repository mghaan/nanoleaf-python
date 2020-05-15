# nanoleaf-python
Nanoleaf Canvas bridge for openHAB written in Python

## About

This is a communication bridge between your [Nanoleaf Canvas](https://nanoleaf.me) lighting and [openHAB](https://www.openhab.org) instance written in Python.

### How it works

The Python bridge uses Nanoleaf API to talk to your Canvas to do the following:

* send commands (e.g. power on/off, set brightness, change color, etc.)
* read status (e.g. power staus, brightness, hue, etc.)
* receive touch events and pass them to openHAB instance

The Python script is easily adjustable for other automation tasks, e.g. talking to [Home Assistant](https://www.home-assistant.io) and other purposes.

## Configuration

All configuration settings are stored in the **nanoleaf.ini** file as explained below. See sample [nanoleaf.ini](https://github.com/mghaan/nanoleaf-python/blob/master/canvas/nanoleaf.ini) file.

    [nanoleaf]
    url = hostname/IP address and port to your Nanoleaf Canvas (e.g. 192.168.1.1:16021)
    token = Canvas auth token
    
    [openhab]
    url = hostname/IP address and port to your openHAB instance (e.g. 192.168.1.1:8080)
    panel = openHAB item that will receive panel ID of the current touch event
    gesture = openHAB item that will received the gesture ID of the current touch event

## Installation

1. Copy both **nanoleaf.ini** and [nanoleaf.py](https://github.com/mghaan/nanoleaf-python/blob/master/canvas/nanoleaf.py) to desired location.
2. (Optional) Copy [nanoleaf.sh](https://github.com/mghaan/nanoleaf-python/blob/master/canvas/nanoleaf.sh) to the same location.

## Usage

### Touch events

To listen and pass touch events, run **nanoleaf.py** without any parameters (or via **nanoleaf.sh**). It will then connect to Nanoleaf and pass any touch events to openHAB.

### Control lights, read state

To control, set or read values from Canvas, use parameters as described below:

**Turn on lights:**

    nanoleaf.py poweron
    
**Turn off lights:**

    nanoleaf.py poweroff
     
**Check if lights are on/off:**

    nanoleaf.py ispower
      
Returns 1 if lights are on, or 0 when off. Note it really means the lights, Nanoleaf is still powered up and connected to your wifi even when the lights are off.

**Set brightness:**

    nanoleaf.py setbright <0-100>
    
**Set saturation:**

    nanoleaf.py setsatur <0-100>
    
**Set hue color:**

    nanoleaf.py sethue <0-360>
    
**Read current brightness level:**

    nanoleaf.py getbright
    
Returns value between 0 (minimum) and 100 (maximum).

**Read current saturation:**

    nanoleaf.py getsatur
    
Returns value between 0 (minimum) and 100 (maximum).

**Read current color:**

    nanoleaf.py gethue

Returns value between 0 and 360. This has meaning only if static scene with single color for all panels is being used.

**Change scene:**

    nanoleaf.py seteffect <name>
    
Name is the scene name as saved in Nanoleaf.

**Get current scene name:**

    nanoleaf.py geteffect
    
Returns the current scene name as saved in Nanoleaf.

### Service mode

You can use [nanoleaf.sh](https://github.com/mghaan/nanoleaf-python/blob/master/canvas/nanoleaf.sh) to run the script as a service and to listen for touch events. It accepts just two parameters: "start" and "stop". On start, it will run the Python script and write its PID into /tmp directory. Or it shuts down (kills) the Python script on stop.



