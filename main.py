'''
Created on 12 Eyl 2023

@author: yusuf
'''

from rest import restObject
import telemetryReader

from struct import unpack
FORMAT = '>B10sBBfffffHB'

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import os
from flask import Flask, render_template,request,jsonify
template_dir = os.path.dirname(__file__)
template_dir = os.path.join(template_dir, 'templates')

app = Flask(__name__,template_folder=template_dir)
 

@app.route('/')
def index():
 
    return render_template('index.html', rockets=rockets)
 
@app.route('/telemetry')
def telemetry(): 
    rocketId = request.args.get('jsdata')  
    telemetryVals = {}
    telemetryVals['status'] = 'not active'
    if rocketId in threads.keys():  
        ret = threads[rocketId].queue.get()  
        while not threads[rocketId].queue.empty():      
            ret = threads[rocketId].queue.get()             
        try:                
            formatedData = unpack(FORMAT, ret)
            jsonData = {}
            jsonData['Altitude'] = formatedData[4]
            jsonData['Speed'] = formatedData[5]
            jsonData['Acceleration'] = formatedData[6]
            jsonData['Thrust'] = formatedData[7]
            jsonData['Temperature'] = formatedData[8]            
            telemetryVals = jsonData
            telemetryVals['status'] = 'active'
        except Exception as e:
            pass
        
        
    return render_template('telemetry.html', telemetryVals=telemetryVals)
 
 
 
@app.route('/rocketDetails')
def rocketDetails(): 
    rocketId = request.args.get('jsdata')  
       
    apiUrl = 'rockets'
    _, rockets = restObject.get(apiUrl=apiUrl)
                  
    details= {}
    for rocket in rockets:
        if 'id' in rocket.keys():
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
     
    apiUrl = 'weather'
    _, weatherResponse = restObject.get(apiUrl=apiUrl)
        
    weather = weatherResponse
    if 'precipitation' in weatherResponse.keys():
        weatherStatus = ""
        for key,val in weatherResponse['precipitation'].items():
            if val == True:
                weatherStatus += f'-{key}'
    
        weather['weatherStatus'] = weatherStatus
        weather['precipitation']['probability'] = weatherResponse['precipitation']['probability']*100           
        weather['humidity']= weatherResponse['humidity']*100

    return render_template('suggestions.html', suggestions=weather)
 
@app.route('/operations')
def operations():
    text = request.args.get('jsdata')
    splittedArr = text.split('#')
    id = splittedArr[0]
    processType = splittedArr[1]
    
    if processType == "launch":
        apiUrl = f"rocket/{id}/status/launched"
        statusCode = restObject.put(apiUrl=apiUrl)        
    elif processType == 'deploy':
        apiUrl = f"rocket/{id}/status/deployed"
        statusCode = restObject.put(apiUrl=apiUrl)
    elif processType == 'cancel':
        apiUrl = f"rocket/{id}/status/launched"
        statusCode = restObject.delete(apiUrl=apiUrl)
       
    print(statusCode)
    if statusCode == 200:
        resp = jsonify({'success': 'Operation is OK'}), statusCode
    else:
        resp = jsonify({'error': 'Operation is NOK'}), statusCode
    return resp
 
rockets = [] 
threads = {}
weather = {}
# main driver function
if __name__ == '__main__':
 
    apiUrl = "rockets"   
    _, rockets = restObject.get(apiUrl=apiUrl)    
            
    for rocket in rockets:
        readerThread = telemetryReader.telemetryReader(rocket['telemetry']['port'],rocket['telemetry']['host'] )
        readerThread.start()
        threads[rocket['id']] = readerThread

    app.run(port=12345)