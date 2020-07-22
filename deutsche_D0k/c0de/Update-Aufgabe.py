#!/usr/bin/python3

# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

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


# bei TheHive4 anmelden
api = TheHiveApi('http://172.17.0.5:9000', '**')


# bei Jira anmelden

username="artsy"
password="**"

jira=JIRA('http://172.17.0.3:8080', basic_auth=(username, password))
response = requests.get("http://172.17.0.3:8080/rest/api/2/search?jql=project=SOC", auth=(username, password))
jj=response.json()

# bei der Datenbank anmelden

connection_dba = pymysql.connect(host='172.17.0.7',
                                 user='root',
                                 password='**',
                                 db='dataframes')

db_data='mysql+mysqldb://'+'root'+':'+'**'+'@'+'172.17.0.7'+':3306/'+'dataframes'+'?charset=utf8mb4'
engine=create_engine(db_data)

get_it=connection_dba.cursor()

 
app=Flask(__name__)
tasks=[]

@app.route("/update/comments", methods=['POST'])


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

        #print("key")
        print(read_file_js['key']['assignee'])
        
        
        ## pana aici merge exact cum treuie

        data=[]
        da=[]
        da={'id': read_file_js['key']['assignee'], 'comments': updated_comment}
        data.append(da)

        df_1_logs=pd.DataFrame(data, columns=['id', 'comments'])
        print(df_1_logs)
        
        print("add df_1 to tablespace...")

        df_1_logs.to_sql('df_1_logs', engine, if_exists='append', index=False)
        
     
        df1_mysql = df_1_logs.to_csv("/app/df_1_logs.csv")

        
        df1_mysql_q=pd.read_csv("/app/df_1_logs.csv")
        print("piece by piece")
        print(df1_mysql_q)

        x=df1_mysql_q['id'].to_string(index=False).strip()
        y=df1_mysql_q['comments'].to_string(index=False).strip()


        #data2 is on the creating alert code
        df2_mysql = get_it.execute('select summary, description from data2 where id = %s', x)
        
        df2_mysql_q = get_it.fetchone()

        df2_mysql_q_d = pd.DataFrame(df2_mysql_q, columns=['mue'])
     
        #print(df2_mysql_q_d)
        #print(df2_mysql_q_d['mue'][0])
        #print(df2_mysql_q_d['mue'][1])
        #print(df2_mysql_q[1])

        print("merge ... ")
     
        df_comm3 = pd.DataFrame({"id": x, "comments": y,  "summary" : [df2_mysql_q_d['mue'][0]]  , "description": [df2_mysql_q_d['mue'][1]] })
        df_comm3.to_csv("/app/df_comm3_single_logs.csv")
        print("send it to mysql table")
        df_comm3.to_sql('df_comm3_logs', engine, if_exists='append', index=False)
        print("export mysql table to csv for applying dataframes")
    
        print("export df_comm3 to csv...")
        df_comm3_mysql=pd.read_sql('SELECT  * from df_comm3_logs ', engine).to_csv("/app/df_comm3_logs.csv")
        print(df_comm3_mysql)

        print("export df_case to csv ..." )

        df_case_csv = pd.read_sql('SELECT * from df_case', engine).to_csv("/app/df_case_logs.csv")
   
        print("create dataframe from df_comm3 and dataframe from df_case.csv")

        df_comm3_csv_single_df = pd.read_csv('/app/df_comm3_single_logs.csv')

        print("summary here to compare")
        print(df_comm3_csv_single_df['summary'])
        df_case_csv_df = pd.read_csv('/app/df_case_logs.csv')
        #df_case_tile = df_case_csv_df['title'].drop_duplicates()


        print("compare if stuff in common")


        is_it = df_case_csv_df.loc[df_case_csv_df['title']==df_comm3_csv_single_df['summary'][0]]
        print(is_it)
    
        if (is_it.shape[0] > 0):

            print("there is a case")

            extract_newdata_case_csv = pd.read_sql('SELECT * from new_data', engine).to_csv('/app/new_data.csv')

            extract_case_csv = pd.read_sql('SELECT * from df_case', engine).to_csv('/app/df_case.csv')
        
            print("convert to dataframe the df_alert csv")

            extract_case_csv_df = pd.read_csv('/app/df_case.csv')
            print(extract_case_csv)

            extract_newdata_case_csv_d = pd.read_csv('/app/new_data.csv')
            print(extract_newdata_case_csv_d)         

            title_case = df_comm3_csv_single_df['summary'].to_string(index=False).strip()
            #print("title case")
            #print(title_case)
            #print("id case")

            find_case_id = extract_case_csv_df.loc[extract_case_csv_df['title'] == df_comm3_csv_single_df['summary'][0]].to_csv('/app/find_case_id.csv')
            print(find_case_id)

            find_case_id_csv_d = pd.read_csv('/app/find_case_id.csv')
            print("here is your bloody case ID")
            print(find_case_id_csv_d['id'][0])
            print("found case ID")

            print(updated_comment)

            find_task_id = extract_newdata_case_csv_d.loc[extract_newdata_case_csv_d['id'] == find_case_id_csv_d['id'][0]] 
            
            taskID_add_1=find_task_id['taskID'].to_string(index=False).strip()
            
            print("this is taskID")

            # Kommentar hinzufügen und neue Protokoll-Dateien einfügen

            json_log = {'message': '{}'.format(updated_comment)  }
            print(json_log)
            print("http://172.17.0.5:9000/api/case/task/{}/log".format(taskID_add_1))

            response_json_log = requests.post("http://172.17.0.5:9000/api/case/task/{}/log".format(taskID_add_1),
                        auth=HTTPBasicAuth('theuser', 'abc123'), data=json_log)
                        
            re11=response_json_log.json()
            print(re11)

     
        return jsonify({'new_comment': updated_comment}), 201

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)

