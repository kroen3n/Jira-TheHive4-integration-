#!/usr/bin/python3

# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import jira
import requests
import pandas as pd
from jira.client import JIRA
import json
from flask import request, jsonify
import subprocess, os
import time
import re
from flask import Flask


import requests
import sys
import time
import uuid
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact, CustomFieldHelper

# log in to TheHive4 with API key
api = TheHiveApi('http://172.17.0.5:9000', '***')

# log in to Jira with credentials (sorry, been lazy!)

username="artsy"
password="***"
jira=JIRA('http://172.17.0.3:8080', basic_auth=(username, password))

#apply JQL query for filtering desired project
response = requests.get("http://172.17.0.3:8080/rest/api/2/search?jql=project=SOC", auth=(username, password))

jj=response.json()


app=Flask(__name__)

tasks=[]


#log in to Jira like in the 90s

username="artsy"
password="***"

jira=JIRA('http://172.17.0.3:8080', basic_auth=(username, password))
response = requests.get("http://172.17.0.3:8080/rest/api/2/search?jql=assignee=artsy", auth=(username, password))
jj=response.json()
#print(response.json())

#to collect our attachments
chici=[]


@app.route("/created/tasks", methods=['POST'])

def create_tickets():

    newreq=request.get_json()
    
    if(len(newreq['issue']['fields']['attachment'])==0):
        print("no attachment in ticket... creating alert with data...")
        new_summary1=newreq['issue']['fields']['summary']
        new_description1=newreq['issue']['fields']['description']
        
        #just in case define one artifact
        artifacts1 = [AlertArtifact(dataType='ip', data='1.2.3.4')]
        
        sourceRef1=str(uuid.uuid4())[0:6]
        
        alert1=Alert(title=new_summary1, 
                     tlp=3, tags=['meh'], 
                     description=new_description1, 
                     type='external', 
                     source='mm2',
                     sourceRef=sourceRef1, 
                     artifacts=artifacts1)
                
        id=None
        response = api.create_alert(alert1)


    if(len(newreq['issue']['fields']['attachment']) > 0):
    
        new_summary=newreq['issue']['fields']['summary']
        new_description=newreq['issue']['fields']['description']
        
        for j in range(0, len(newreq['issue']['fields']['attachment'])):
            new_content = newreq['issue']['fields']['attachment'][j]['content']
            repl_content=re.sub('localhost', '172.17.0.3', new_content)
            name_attachment = newreq['issue']['fields']['attachment'][j]['filename']
            subprocess.call(["curl", "-u", "artsy:***",  
            "{}".format(repl_content), "--output",
            "{}".format(name_attachment)], 
            shell = False)
    
            ki = {'ki': name_attachment, 'summary':new_summary}
            print(ki)

            chici.append(ki)
            df_chi = pd.DataFrame(chici)
       
        artifacts = [ ]

        for jj in range(df_chi.shape[0]):
                #print("here are all...")
                #print(df_chi['ki'][jj])

                addedartifacts = AlertArtifact(dataType='file', data='{}'.format(df_chi['ki'][jj]))       
                artifacts.append(addedartifacts)


        print("=====================================")
        print(artifacts)
        print("=====================================")

# alert preparation

        sourceRef = str(uuid.uuid4())[0:6]
        alert = Alert(title=new_summary,
            tlp=3,
            tags=['lelol'],
            description=new_description,
            type='external',
            source='mm1',
            sourceRef=sourceRef,
            artifacts=artifacts)

# alert creation
        id = None
        response = api.create_alert(alert)


    return jsonify({'tasks':tasks}), 201


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
