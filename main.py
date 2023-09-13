'''
Created on 12 Eyl 2023

@author: yusuf
'''

import requests
import telemetryReader

from struct import unpack, calcsize
FORMAT = '>B10sBBfffffHB'

# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
import os
from flask import Flask, render_template, flash, redirect, url_for,request,jsonify
template_dir = os.path.dirname(__file__)
template_dir = os.path.join(template_dir, 'templates')
print(template_dir)
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__,template_folder=template_dir)
 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index():
 
    return render_template('asd.html', rockets=rockets)
 
@app.route('/telemetry')
def telemetry(): 
    rocketId = request.args.get('jsdata')  
    ret = {}
    if rocketId in threads.keys(): 
        ret = threads[rocketId].queue.get()
        formatedData = unpack(FORMAT, ret)
        jsonData = {}
        jsonData['Altitude'] = formatedData[4]
        jsonData['Speed'] = formatedData[5]
        jsonData['Acceleration'] = formatedData[6]
        jsonData['Thrust'] = formatedData[7]
        jsonData['Temperature'] = formatedData[8]
        ret = jsonData
        
    return render_template('telemetry.html', telemetryVals=ret)
 
 
 
@app.route('/rocketDetails')
def rocketDetails(): 
    rocketId = request.args.get('jsdata')  
    ret = {}
    apiUrl = "http://localhost:5000/rockets"
    response = requests.get(apiUrl, headers={"X-API-Key":"API_KEY_1"})
    rockets = response.json()
    
    details= {}
    for rocket in rockets:
        if rocket['id'] == rocketId:
            details['status'] = rocket['status']
            details['mass'] = rocket['mass']
            details['launched-Time'] = rocket['timestamps']['launched']
            details['deployed-Time'] = rocket['timestamps']['deployed']
            details['failed-Time'] = rocket['timestamps']['failed']
            details['cancelled-Time'] = rocket['timestamps']['cancelled']
            
            details['altitude'] = rocket['altitude']
            details['speed'] = rocket['speed']
            details['acceleration'] = rocket['acceleration']
            details['thrust'] = rocket['thrust']
            details['temperature'] = rocket['temperature']
            break
        
    return render_template('rocketDetails.html', details=details) 
 
@app.route('/weather')
def suggestions():
    text = request.args.get('jsdata')

    apiUrl = "http://localhost:5000/weather"
    response = requests.get(apiUrl, headers={"X-API-Key":"API_KEY_1"})
    weather = response.json()
    
    if 'precipitation' in weather.keys():
        weatherStatus = ""
        for key,val in weather['precipitation'].items():
            if val == True:
                weatherStatus += f'-{key}'
    
        weather['weatherStatus'] = weatherStatus
        weather['precipitation']['probability'] = weather['precipitation']['probability']*100
        
        weather['humidity']= weather['humidity']*100

    return render_template('suggestions.html', suggestions=weather)
 
@app.route('/operations')
def operations():
    text = request.args.get('jsdata')
    splittedArr = text.split('#')
    id = splittedArr[0]
    processType = splittedArr[1]
    
    if processType == "launch":
        apiUrl = f"http://localhost:5000/rocket/{id}/status/launched"
        response = requests.put(apiUrl, headers={"X-API-Key":"API_KEY_1"})
    elif processType == 'deploy':
        apiUrl = f"http://localhost:5000/rocket/{id}/status/deployed"
        response = requests.put(apiUrl, headers={"X-API-Key":"API_KEY_1"})
    elif processType == 'cancel':
        apiUrl = f"http://localhost:5000/rocket/{id}/status/launched"
        response = requests.delete(apiUrl, headers={"X-API-Key":"API_KEY_1"})
    
    print(response)
    message = {'text' : 'OP SUC'}
    
    return jsonify(message), 200
 
rockets = [] 
threads = {}
# main driver function
if __name__ == '__main__':
 
    apiUrl = "http://localhost:5000/rockets"
    response = requests.get(apiUrl, headers={"X-API-Key":"API_KEY_1"})
    rockets = response.json()
    
    for rocket in rockets:
        readerThread = telemetryReader.telemetryReader(rocket['telemetry']['port'],rocket['telemetry']['host'] )
        readerThread.start()
        threads[rocket['id']] = readerThread
   
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(port=12345)