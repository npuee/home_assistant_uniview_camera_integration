#!/usr/bin/python3
import sys
import json
import requests
from requests.auth import HTTPDigestAuth # NVR Digest auth
from multiprocessing.dummy import Pool as ThreadPool # Multicore fastapi requests
import pip # Runtime install fastapi, if not installed 
import socket # To check if nvr port 80 is reachable.
import time
start_time = time.time() # measure runtime


#Device setting:
cctv={
    "user" : "username",
    "password" : "password",
    "timeout" : 10,
    "cameras": {
        "camera_ip" : {"rule" : "IntrusionDetection"},
        "camera_ip" : {"rule" : "IntrusionDetection"},
    }
}

#
#
# DO NOT EDIT BELOW
#
#

# Install fastapi if not installed. Usefull when container image updates.
def import_with_auto_install(package):
    try:
        return __import__(package)
    except ImportError:
        pip.main(['install', package])
    return __import__(package)

import_with_auto_install('fastapi')
from fastapi import APIRouter, FastAPI, Header, Request, HTTPException



# Static nvr urls
camera_prefix = "/LAPI/V1.0/Smart/"

#Params
function_to_run = sys.argv[1]
pool = ThreadPool(8)


# Set payload for camera detection ON or OFF        
if function_to_run == "off":
    payload = {"Enabled": 0}
else:
    payload = {"Enabled": 1}

#
# Get camera detection status
# 
def detection_status(camera):
    # Combine url
    camera_url = "http://" + camera + camera_prefix + cctv["cameras"][camera]["rule"] + "/Rule"
    # get camera detection rule status

    try:
        camera_query = requests.get(camera_url, auth=HTTPDigestAuth(cctv["user"], cctv["password"]), timeout=cctv["timeout"])
        camera_result = camera_query.json()
        return  camera_result["Response"]["Data"]["Enabled"]   
    except:
        print("Camera %s timeout!" % camera)
        return 0

# Get camera detection status
if function_to_run == "status":
    results = pool.map(detection_status, cctv["cameras"])
    enabled_count = sum(results)
    total_cameras = len(cctv["cameras"])
    runtime = round((time.time() - start_time), 2)

    if enabled_count == 0:
        #print(f"Status: {enabled_count}/{total_cameras} cameras enabled. Runtime: {runtime} second.")
        exit(1)
    elif 0 < enabled_count < total_cameras:
        print(f"Status: {enabled_count}/{total_cameras} cameras enabled (partial). Runtime: {runtime} second.")
        exit(0)
    else:
        #print(f"Status: {enabled_count}/{total_cameras} cameras enabled (all on). Runtime: {runtime} second.")
        exit(0)

# Set camera detection status
def switch_detection(camera):
    # Combine url
    camera_url = "http://" + camera + camera_prefix + cctv["cameras"][camera]["rule"] + "/Rule"
    # Set camera detection rule status
    camera_query = requests.put(camera_url,  data=json.dumps(payload), auth=HTTPDigestAuth(cctv["user"], cctv["password"]), timeout=cctv["timeout"])
    return camera_query.json()



# Set detection based on payload
pool.map(switch_detection, cctv["cameras"])
print("NVR status change runtime: %s second." % round((time.time() - start_time), 2))
