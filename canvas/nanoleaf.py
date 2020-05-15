#!/usr/bin/python3

import configparser
import logging
import json
import requests
import sys
import time

#
# parse ini file and check parameters
#
try:
   config = configparser.ConfigParser()
   config.read(sys.path[0] + "/nanoleaf.ini")
except:
   print("Configuration parse error!")
   sys.exit(1)

for section in {"nanoleaf", "openhab"}:
   if section not in config:
      print("Section " + section + " not defined!")
      sys.exit(1)
   parameter = {"url", "token"}
   if section == "openhab":
      parameter = {"url", "panel", "gesture"}
   for param in parameter:
      if param not in config[section]:
         print("Parameter " + section + ":" + param + " not defined!")
         sys.exit(1)
         if config[section][param] == "":
            print("Parameter " + section + ":" + param + " is empty!")
            sys.exit(1)

#
# variables
#
cfgNanoleafUrl = "http://" + config['nanoleaf']['url'] + "/api/v1/" + config['nanoleaf']['token'] + "/"
cfgOpenhabUrl = "http://" + config['openhab']['url'] + "/rest/items/"

headersJson = { "Accept": "application/json",  "Content-Type": "application/json" }
headersMixed = { "Accept": "application/json", "Content-Type": "text/plain" }

connTimeout = 10
connRetry = 2
connDelay = 5

#
# connect to canvas
#
def connectToCanvas():
   global response
   global rr
   global newlineSeen

   loop = 0
   while (True):
      loop = loop + 1
      try:
         response = requests.get(cfgNanoleafUrl + "events?id=4", headers = headersMixed, stream = True)
         logging.info("Listening...")
         rr = ""
         newlineSeen = False
         break
      except:
         if loop > connRetry:
            logging.info("Connection error.")
            sys.exit(10)
         else:
            logging.info("Connection failed. Retrying " + str(loop) + "/" + str(connRetry) + " ...")
            time.sleep(connDelay)

#
# parse single event (e.g. swipe, touch)
#
def parseEvent():
   global rr

   # throw away no JSON part (is always id=4)
   rr = rr[12:]
   logging.info(rr)
   loaded_json = json.loads(rr)
   gesture = loaded_json['events'][0]['gesture']
   panelId = loaded_json['events'][0]['panelId']
   try:
      requests.post(cfgOpenhabUrl + config['openhab']['panel'], headers = headersMixed, data = str(panelId), timeout = connTimeout)
      requests.post(cfgOpenhabUrl + config['openhab']['gesture'], headers = headersMixed, data = str(gesture), timeout = connTimeout)
   except:
      logging.info("openHAB communication error.")

#
# read events from canvas
#
def processEvents():
   global response
   global rr
   global newlineSeen

   # parse every single byte received until /n/n
   r = response.raw.read(1)
   r = r.decode("utf-8")
   # connection was lost, re-connect
   if len(r) == 0:
      logging.info("Connection lost. Reconnecting...")
      connectToCanvas()
   else:
      if newlineSeen:
         if r == "\n":
            parseEvent()
            newlineSeen = False
            # start over
            rr = ""
         else:
            newlineSeen = False
            rr = rr+r
      else:
         if r == "\n":
            newlineSeen = True
            # replace \n with space
            rr = rr + " "
         else:
            rr = rr + r

#
# send command to canvas
#
def sendCommand(uri, datas):
   loop = 0
   while (True):
      loop = loop + 1
      try:
         requests.put(cfgNanoleafUrl + uri, headers = headersJson, data = str(datas), timeout = connTimeout)
         print("OK")
         break
      except:
         if loop > connRetry:
            print("")
         else:
            logging.info("Connection failed. Retrying " + str(loop) + "/" + str(connRetry) + " ...")
            time.sleep(connDelay)

#
# read and process value from canvas
#
def readValue(uri):
   loop = 0
   while (True):
      loop = loop + 1
      try:
         response = requests.get(cfgNanoleafUrl + uri)
         data = json.loads(response.text)
         print(data)
         break
      except:
         if loop > connRetry:
            print("")
         else:
            logging.info("Connection failed. Retrying " + str(loop) + "/" + str(connRetry) + " ...")
            time.sleep(connDelay)

#
# read plain value from canvas
#
def readPlain(uri):
   loop = 0
   while (True):
      loop = loop + 1
      try:
         response = requests.get(cfgNanoleafUrl + uri)
         data = response.text.replace('"', '')
         print(data)
         break
      except:
         if loop > connRetry:
            print("")
         else:
            logging.info("Connection failed. Retrying " + str(loop) + "/" + str(connRetry) + " ...")
            time.sleep(connDelay)

#
# handle command line parameters
#
if len(sys.argv) > 1:
   if sys.argv[1] == "poweron":
      sendCommand("state", "{ \"on\": { \"value\": true } }")

   elif sys.argv[1] == "poweroff":
      sendCommand("state", "{ \"on\": { \"value\": false } }")

   elif sys.argv[1] == "ispower":
      readValue("state/on")

   elif sys.argv[1] == "setbright":
      sendCommand("state", "{ \"brightness\": { \"value\": " + sys.argv[2] + " } }")

   elif sys.argv[1] == "getbright":
      readValue("state/brightness")

   elif sys.argv[1] == "setsatur":
      sendCommand("state", "{ \"sat\": { \"value\": " + sys.argv[2] + " } }")

   elif sys.argv[1] == "getsatur":
      readValue("state/sat")

   elif sys.argv[1] == "sethue":
      sendCommand("state", "{ \"hue\": { \"value\": " + sys.argv[2] + " } }")

   elif sys.argv[1] == "gethue":
      readValue("state/hue")

   elif sys.argv[1] == "seteffect":
      res = sys.argv[2]
      res = res.replace("_", " ")
      sendCommand("effects", "{ \"select\": \"" + res + "\" }")

   elif sys.argv[1] == "geteffect":
      readPlain("effects/select")

#
# read events from canvas if no parameter given
#
else:
   logging.basicConfig(level = logging.INFO, format = "%(asctime)s %(message)s")
   connectToCanvas()
   while True:
      processEvents()