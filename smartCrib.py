#!/usr/bin/python

import urllib
import time
import ssl
import logging
import json
import datetime
import re

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def createJsonArray():
	mainLink = "http://phuocandlilianfamily.com/MFile.txt"
	wearLink = "http://phuocandlilianfamily.com/WFile.txt"

	mainFile = urllib.urlopen(mainLink)
	wearFile = urllib.urlopen(wearLink)
	dataArray = []

	for line in mainFile:
		if 'TEMP' in line:
			dataArray.append(getNum(line))
		if 'W' in line:
			dataArray.append(getNum(line))
		if 'C' in line:
			dataArray.append(getNum(line))

	for line in wearFile:
		if 'HR' in line:
			dataArray.append(getNum(line))
		if "M" in line:
			dataArray.append(getNum(line))


	now_str = datetime.datetime.now().strftime('%Y:%m:%d:%H:%M:%S')
	message = {}
	messageJsonArray = []
	datatypeArray = ['temperature', 'weight', 'cry', 'heartrate', 'motion'] 

	for i in range (5):
		message['datatype'] = datatypeArray[i]
		message['data'] = dataArray[i]
		message['timestamp'] = now_str
		messageJsonArray.append(json.dumps(message))

	return messageJsonArray

def getNum(line):

	myStr =  re.findall(r'[\d\.\d]+', line)
	return myStr[0]

def main():

	myMQTTClient = None
	myMQTTClient = AWSIoTMQTTClient("smartcrib")
	myMQTTClient.configureEndpoint("aho7m8kcsddgh.iot.us-east-1.amazonaws.com", 8883)
	myMQTTClient.configureCredentials("/home/pi/Downloads/rootCA.pem","/home/pi/Downloads/0f8c0159f5-private.pem.key","/home/pi/Downloads/0f8c0159f5-certificate.pem.crt")

#myMQTTClient.configureOfflinePublishQueueing(-1)
#myMQTTClient.configureDrainingFrequency(2)
#myMQTTClient.configureConnectDisconnectTimeout(10)
#myMQTTClient.configureMQTTOperationTimeout(5)


	messageJsonArray = createJsonArray()

	myMQTTClient.connect()
	for i in range(5):
		myMQTTClient.publish("smartCrib", messageJsonArray[i], 0)

	myMQTTClient.disconnect()

main();
