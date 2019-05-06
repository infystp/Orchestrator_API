# -*- coding: utf-8 -*-
"""
Created on Mon May  6 11:10:35 2019

@author: Hima_Gundlapalli
"""

import requests
from flask import Flask,request,make_response
import os,json

app = Flask(__name__)

#To be modified based on the process to run
releaseKey = None
#processKey = 'Testing1'
#processId = 100013

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    
    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

#processing the request from dialogflow
def processRequest(req):
    
    result = req.get("result")
    print(result)
    
    parameters = result.get("parameters")
    print(parameters)
    
    processId = parameters.get("number")
    
    processKey = parameters.get("any")
    
    #Authentication request to get the access token
    urlgetAuthenticationToken = 'https://platform.uipath.com/api/Account/Authenticate'
    body = {"tenancyName": "viswanadha_parcha", "usernameOrEmailAddress": "admin", "password": "Jan@2019"}
    headers = {'content-type': 'application/json'}
    respAuthentication = requests.post(urlgetAuthenticationToken, data=json.dumps(body), headers=headers)
    print('Authentication Status: ',respAuthentication.status_code)
    print('--------------------------------------------')
    parsed_json_token = json.loads(respAuthentication.text)
    print('Authentication token: ',parsed_json_token['result'])
    json_token = parsed_json_token['result']
    
    #Getting Robos
    urlGetRobos = 'https://platform.uipath.com/odata/Robots'
    respRobots = requests.get(urlGetRobos, headers={'Content-Type':'application/json', 'Authorization': 'Bearer {}'.format(json_token)})
    print('Robos Status: ',respRobots.status_code)
    print('Robos Response: ',respRobots.text)
    print('--------------------------------------------')
    
    #Getting Release Keys
    urlGetReleaseKey = 'https://platform.uipath.com/odata/Releases'
    respRleaseKey = requests.get(urlGetReleaseKey, headers={'Content-Type':'application/json', 'Authorization': 'Bearer {}'.format(json_token)})
    
    #Getting Correct Release Key from Collection by Process Id and Process Name
    strRobots = respRleaseKey.text
    
    print(respRleaseKey.text)
    print('--------------------------------------------')
    strformattedRelease = r''+ strRobots +''
    
    json_Release = json.loads(strformattedRelease)
    
    #Converting multi level list to string to load into json again
    jsontostring_ReleaseValueList = json.dumps(json_Release['value'])
    str_ReleaseValueList = json.loads(jsontostring_ReleaseValueList)
    
    for elements in str_ReleaseValueList: 
        print('Process Id:' ,elements['Id'])
        print('--------------------------------------------')
        if elements['ProcessKey'] == processKey and elements['Id'] == processId:
            releaseKey = elements['Key']
            break
    
    
    releaseKey = releaseKey.strip().replace("\"","")
    print('Release Key with Process Id {}, Process Name {} is:{} '.format(processId,processKey,releaseKey))
    print('--------------------------------------------')
    
    #Starting job
    urlStartJobs = 'https://platform.uipath.com/odata/Jobs/UiPath.Server.Configuration.OData.StartJobs'
    body = { "startInfo": {
        "ReleaseKey": releaseKey,
        "Strategy": "All",
        "RobotIds": [],
        "NoOfRobots": 0
      }}
    
    respStartJobs = requests.post(urlStartJobs, headers={'Content-Type':'application/json', 'Authorization': 'Bearer {}'.format(json_token)},data=json.dumps(body))
    print('Start Job Status: ',respStartJobs.status_code)
    print('Start job Response',respStartJobs.text)
    
    speech = "Response JSON: "+respStartJobs.text + "Response Status: "+ respStartJobs.status_code
    
    return {
        "speech": speech,
        "displayText": speech,
        "source": "dialogflow-OrchestratorAPI"
        }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5050))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
