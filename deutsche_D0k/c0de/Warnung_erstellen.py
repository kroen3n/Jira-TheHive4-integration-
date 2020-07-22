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
from requests.auth import HTTPBasicAuth
from pandas import json_normalize

from flask import Flask

import pymysql
from sqlalchemy import create_engine


import requests
import sys
import time
import uuid
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact, CustomFieldHelper

api = TheHiveApi('http://172.17.0.5:9000', '**')


username="artsy"
password="**"
jira=JIRA('http://172.17.0.3:8080', basic_auth=(username, password))

response = requests.get("http://172.17.0.3:8080/rest/api/2/search?jql=project=SOC", auth=(username, password))
jj=response.json()

global new_summary

app=Flask(__name__)
tasks=[]

data22=[]
data=[]
da=[]

username="artsy"
password="**"
jira=JIRA('http://172.17.0.3:8080', basic_auth=(username, password))
response = requests.get("http://172.17.0.3:8080/rest/api/2/search?jql=assignee=artsy", auth=(username, password))
jj=response.json()
#print(response.json())

ress = response.json()

open_issue=jira.search_issues('project=\"soc\" ',  fields='comment, attachment', json_result=True)


connection_dba = pymysql.connect(host='172.17.0.7',
        user='root',
        password='**',
        db='dataframes')

db_data='mysql+mysqldb://'+'root'+':'+'**'+'@'+'172.17.0.7'+':3306/'+'dataframes'+'?charset=utf8mb4'
engine=create_engine(db_data)

get_it=connection_dba.cursor()

chici=[]

@app.route("/created/tasks", methods=['POST'])

def create_tickets():
    newreq=request.get_json()
    if(len(newreq['issue']['fields']['attachment'])==0):
        print("no attachment in ticket... creating alert with data...")
        new_summary1=newreq['issue']['fields']['summary']
        new_description1=newreq['issue']['fields']['description']
        new_key = newreq['issue']['key']

        # diese Daten in den Tablespace data2 senden 
        print(new_key)

        data2=[]
        da2=[]

        da2={"summary":new_summary1, "description": new_description1, "id": new_key}
        data2.append(da2)

        print(data2)

        df_2=pd.DataFrame(data2, columns=['summary', 'description', 'id'])
        df_2.to_sql('data2', engine, if_exists='append', index=False)

        df_2.to_sql('data2_logs', engine, if_exists='append', index=False)


        artifacts1 = [AlertArtifact(dataType='ip', data='1.2.3.4')]
        sourceRef1=str(uuid.uuid4())[0:6]
        
        alert1=Alert(title=new_summary1, tlp=3, tags=['meh'], 
                description=new_description1, type='external', 
                source='mm2',
                sourceRef=sourceRef1, 
                artifacts=artifacts1)
                
        id=None
        response = api.create_alert(alert1)

        print(response)

        url_alert="http://172.17.0.5:9000/api/alert/"
        response_hive4_alert = requests.get(url_alert, auth=HTTPBasicAuth('theuser', '**'))
        data_hive4_alert=response_hive4_alert.json()

        data_normalize_alert=json_normalize(data=data_hive4_alert)
        print("data normalize alert from hive4")
        print(data_normalize_alert[['id', 'title']])

        if(data_normalize_alert.shape[0]==0):
            print("any alert created yet?!")
        else:
            data22=data_normalize_alert[['id', 'title']]
            df_alert=pd.DataFrame(data22)
            df_alert.to_sql('df_alert', engine, if_exists='replace', index=False)
           
            data22_logs=data_normalize_alert[['id', 'title']]
            df_alert_logs = pd.DataFrame(data22_logs) 
            df_alert_logs.to_sql('df_alert_logs', engine, if_exists='replace', index=False)

            #df_alert_mysql=pd.read_sql('select * from df_alert', engine)

        #here to add data_normalize_case

        url_case="http://172.17.0.5:9000/api/case/"
        response_hive4_case = requests.get(url_case, auth=HTTPBasicAuth('theuser', '**'))
        data_hive4_case = response_hive4_case.json()
        data_normalize_case = json_normalize(data=data_hive4_case)

        print("getting data from new cases")
        data21=data_normalize_case[['id', 'title']]
        df_case=pd.DataFrame(data21)
        df_case.to_sql('df_case', engine, if_exists='append', index=False)

        data21_logs = data_normalize_case[['id', 'title']]
        df_case_logs = pd.DataFrame(data21_logs)
        df_case_logs.to_sql('df_case_logs', engine, if_exists='append', index=False)


    if(len(newreq['issue']['fields']['attachment']) > 0):

        new_summary=newreq['issue']['fields']['summary']
        new_description=newreq['issue']['fields']['description']
        for j in range(0, len(newreq['issue']['fields']['attachment'])):
            new_content = newreq['issue']['fields']['attachment'][j]['content']
            repl_content=re.sub('localhost', '172.17.0.3', new_content)
            name_attachment = newreq['issue']['fields']['attachment'][j]['filename']
            subprocess.call(["curl", "-u", "artsy:abc123",  "{}".format(repl_content), "--output", "{}".format(name_attachment)], shell = False)
    
            ki = {'ki': name_attachment, 'summary':new_summary}
            print(ki)

            chici.append(ki)
            df_chi = pd.DataFrame(chici)

        artifacts = [
           # AlertArtifact(dataType='file', data='users.csv')
            ]

        for jj in range(df_chi.shape[0]):
             
                #print(df_chi['ki'][jj])

                addedartifacts = AlertArtifact(dataType='file', data='{}'.format(df_chi['ki'][jj]))
       
                artifacts.append(addedartifacts)

        print("=====================================")
        print(artifacts)
        print("=====================================")

# die Probe für die Erstellung des Warnung vorbereiten

        sourceRef = str(uuid.uuid4())[0:6]
        alert = Alert(title=new_summary,
            tlp=3,
            tags=['lelol'],
            description=new_description,
            type='external',
            source='mm1',
            sourceRef=sourceRef,
            artifacts=artifacts)

# die Warnung erstellen
        id = None
        response = api.create_alert(alert)
 
    return jsonify({'tasks':tasks}), 201

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)