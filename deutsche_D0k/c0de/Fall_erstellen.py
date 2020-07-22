#!/usr/bin/python3


# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import os
from urllib.request import urlopen
import jira
import re
import requests
import pandas as pd
from jira.client import JIRA
import json
from flask import request, jsonify
from requests.auth import HTTPBasicAuth
from pandas import json_normalize
import numpy as np
import pymysql
import subprocess
from sqlalchemy import create_engine

from flask import Flask

import requests
import sys
import time
import uuid
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact, CustomFieldHelper


# access to TheHive4
api = TheHiveApi('http://172.17.0.5:9000', '**')



# access to Jira
username="artsy"
password="**"
jira=JIRA('http://172.17.0.3:8080', basic_auth=(username, password))
response = requests.get("http://172.17.0.3:8080/rest/api/2/search?jql=project=SOC", auth=(username, password))
jj=response.json()

#access to dba

connection_dba = pymysql.connect(host='172.17.0.7',
                                 user='root',
                                 password='**',
                                 db='dataframes')

db_data='mysql+mysqldb://'+'root'+':'+'**'+'@'+'172.17.0.7'+':3306/'+'dataframes'+'?charset=utf8mb4'
engine=create_engine(db_data)

get_it=connection_dba.cursor()

### ugh...
 
app=Flask(__name__)
tasks=[]


@app.route("/get/comments", methods=['POST'])


def hehe():


        up=request.data
        update_req = json.loads(up)
        print(update_req)


        df_updated=pd.DataFrame(update_req)
        print(df_updated)

        print("new_comment from dataframe")

        updated_comment=df_updated['comment']['body']
        print(updated_comment)

        sel = df_updated['comment']['self']
        print(sel)

        url_sel = sel.split('/')
        print(url_sel)
        print(url_sel[7])

        new_url = sel.rsplit("/", 2)[0]
        print(new_url) 

        updated_url = re.sub('localhost', '172.17.0.3', new_url)

        take_file = subprocess.call(["curl", "-u", "artsy:**", "{}".format(updated_url), "--output", "/app/new.json"], shell=False)

        read_file_js = pd.read_json('/app/new.json')
        print(read_file_js)
        print("expand and so on...")

        print(read_file_js['expand'])

        print("")


        print("==========description========")
        print(read_file_js['fields']['description'])

        print("==========summary==========")
        print(read_file_js['fields']['summary'])

        print("keeyyyyyyyyyyyyy")
        print(read_file_js['key']['assignee'])
        
        
        ## pana aici merge exact cum treuie

        data=[]
        da=[]

        da={'id': read_file_js['key']['assignee'], 'comments': updated_comment}
        data.append(da)

        df_1=pd.DataFrame(data, columns=['id', 'comments'])
        print("this is where you add new collected data")
        print(df_1)
        
        print("add df_1 to tablespace...")

        df_1.to_sql('df_1', engine, if_exists='append', index=False)
     
        df1_mysql = df_1.to_csv("/app/df_1.csv")
        
        df1_mysql_q=pd.read_csv("/app/df_1.csv")
        print("piece by piece")
        print(df1_mysql_q)

        x=df1_mysql_q['id'].to_string(index=False).strip()
        y=df1_mysql_q['comments'].to_string(index=False).strip()

        df2_mysql = get_it.execute('select summary, description from data2 where id = %s', x)
        
        df2_mysql_q = get_it.fetchone()
        print(df2_mysql_q)
        print("piece by piece")

        df2_mysql_q_d = pd.DataFrame(df2_mysql_q, columns=['mue'])

        print("merge")
        df_comm3 = pd.DataFrame({"id": x, "comments": y, 
        "summary" : [df2_mysql_q_d['mue'][0]] , "description": [df2_mysql_q_d['mue'][1]] })
        print("i pased here...")


        #print(df_comm3)
        df_comm3.to_csv("/app/df_comm3_single.csv")
        print("send it to mysql table")

        df_comm3.to_sql('df_comm3', engine, if_exists='append', index=False)

        print("export mysql table to csv for applying dataframes")

    
        print("export df_comm3 to csv...")
        df_comm3_mysql=pd.read_sql('SELECT  * from df_comm3 ', engine).to_csv("/app/df_comm3.csv")
        print(df_comm3_mysql)

        print("export df_case to csv ..." )

        df_case_csv = pd.read_sql('SELECT * from df_case', engine).to_csv("/app/df_case.csv")
    
        print("create dataframe from df_comm3 and dataframe from df_case.csv")

        df_comm3_csv_single_df = pd.read_csv('/app/df_comm3_single.csv')

        print("summary here to compare")
        print(df_comm3_csv_single_df['summary'])
        df_case_csv_df = pd.read_csv('/app/df_case.csv')
        #df_case_tile = df_case_csv_df['title'].drop_duplicates()


        print("compare if stuff in common")

        is_it = df_case_csv_df.loc[df_case_csv_df['title']==df_comm3_csv_single_df['summary'][0]]
    
        if (is_it.shape[0] == 0):

            print("always create a case")

            extract_alert_csv = pd.read_sql('SELECT * from df_alert', engine).to_csv('/app/df_alert.csv')
        
            print("convert to dataframe the df_alert csv")

            extract_alert_csv_df = pd.read_csv('/app/df_alert.csv')
            print(extract_alert_csv_df)
            
            # Alarm-ID erhalten

            title_case = df_comm3_csv_single_df['summary'].to_string(index=False).strip()
            print(title_case)

            find_alert=extract_alert_csv_df[extract_alert_csv_df['title'] == df_comm3_csv_single_df['summary'][0]] 
            print(find_alert)

            print("here find the id")
            val21 = find_alert['id'].to_string(index=False).strip()

            print(val21)
            
            # neuen Fall und Aufgabe erstellen
            
            response_create_case=requests.post("http://172.17.0.5:9000/api/alert/{}/createCase".format(val21),
                   auth=HTTPBasicAuth('theuser', '**'))

            print("response creation")
            print(response_create_case)
            data_create_case2=response_create_case.json()
            print(data_create_case2)
            id_case_readable2=data_create_case2['id']

            print("create new task for new case id")

            new_json_task2={'title': 'Jira comments'}

            response_create_new_task2=requests.post("http://172.17.0.5:9000/api/case/{}/task".format(id_case_readable2),
                    auth=HTTPBasicAuth('theuser', '**'), data=new_json_task2)

            new_repopo2=response_create_new_task2.json()

            new_df_task_id2=new_repopo2['id']

            didi22 = pd.DataFrame( { 'id':[id_case_readable2], 'taskID':[new_df_task_id2] } )

            #print(didi22)

            didi22.to_sql('new_data', engine, if_exists='append', index=False)

            print("add logs to new task")
            comix22 = df_comm3_csv_single_df['comments'].to_string(index=False).strip()

            json_log_new2={'message': '{}'.format(comix22)}

            response_json_log_new2 = requests.post("http://172.17.0.5:9000/api/case/task/{}/log".format(new_df_task_id2),
                  auth=HTTPBasicAuth('theuser', '**'), data=json_log_new2)
            re112new=response_json_log_new2.json()

        #neuen Fall zum Tablespace df_case hinzufügen
        
            dfa=[]
            dfapp=[]

            dfa={"id": id_case_readable2, "title": title_case }
            
            dfapp.append(dfa)
            df_app=pd.DataFrame(dfapp, columns=['id', 'title'])
            df_app.to_sql('df_case', engine, if_exists='append', index=False)
            df_app.to_sql('df_case_logs', engine, if_exists='append', index=False)
            
        else:
            print("case is already created")
            
            
        return jsonify({'new_comment': updated_comment}), 201
        
if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
