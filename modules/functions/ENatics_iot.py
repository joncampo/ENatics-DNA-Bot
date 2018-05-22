#!/usr/bin/env python
import requests
import json
import time
import sys
import os



###########################################################################
def iot_map_download(google_map_key,latitude,longitude):
    #api = "/network-device"
    image_exists=os.path.isfile('temp/map_temp_sensor.png')

    if image_exists is True:
        #copy to map.png
        print ("Image exists!")
        return True

    else:
        print ("Image does not exist!")
        url = "https://maps.googleapis.com/maps/api/staticmap"
        querystring = {"markers": str(latitude)+","+str(longitude),"zoom":"12","size":"250x250","key":google_map_key}
        headers = {'Cache-Control': 'no-cache'}
        result = requests.get(url, headers=headers, params=querystring, verify=False, timeout=3).content
        with open('temp/map_temp_sensor.png', 'wb') as handler:
            handler.write(result)

        if result:
            return True
            
        else:
            return False

def iot_coordinate():
	FULL_URL = "http://pg-api.sensorup.com/OGCSensorThings/v1.0/Observations(309954)/FeatureOfInterest"
	result = requests.get(FULL_URL, verify=False, timeout=3).json()

	longitude=result["feature"]["coordinates"][0]
	latitude=result["feature"]["coordinates"][1]

	return longitude,latitude


def iot_temperature(iot_key):
	FULL_URL = "https://pg-api.sensorup.com/st-playground/proxy/v1.0/Datastreams(309908)/Observations"
	headers = {  "Content-Type":"application/json",
				"St-P-Access-Token": iot_key}
	result = requests.get(FULL_URL, headers=headers, verify=False,timeout=3).json()

	time=result["value"][0]["phenomenonTime"]
	temperature=result["value"][0]["result"]

	return temperature,time