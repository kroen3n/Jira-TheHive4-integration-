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

from mysql_login import ConnectMySQL

from jira_login import JiraLogin

from script_cred import HostTheHive
from script_cred import HostJira
from script_cred import HostDBA


from script_cred import PasswdDBA
from script_cred import PasswdTheHive
from script_cred import PasswdJira

from script_cred import UserJira
from script_cred import UserTheHive
from script_cred import UserDBA


# access to TheHive4
api = TheHiveApi('http://{}:9000'.format(HostTheHive.hostname), '***')

 
app=Flask(__name__)
tasks=[]


@app.route("/update/comments", methods=['POST'])


def hehe():

        class Update:
        
            up=request.data
            update_req = json.loads(up)
            print(update_req)
            df_updated=pd.DataFrame(update_req)
            print(df_updated)
            print("new_comment from dataframe")
            updated_comment=df_updated['comment']['body']
            print(updated_comment)


        class Link:

            sel = Update.df_updated['comment']['self']
            print(sel)
            url_sel = sel.split('/')
            new_url = sel.rsplit("/", 2)[0]
            updated_url = re.sub('localhost', '{}'.format(HostJira.hostname), new_url)


        class Extract:

            take_file = subprocess.call(["curl", "-u", "{0}:{1}".format(UserJira.name, PasswdJira.secret), 
                "{}".format(Link.updated_url), "--output", "/app/new.json"], shell=False)

            read_file_js = pd.read_json('/app/new.json')


        class Fields:
        
            data=[]
            da=[]

            da={'id': Extract.read_file_js['key']['assignee'], 'comments': Update.updated_comment}
            data.append(da)

            df_1_logs=pd.DataFrame(data, columns=['id', 'comments'])
            df_1_logs.to_sql('df_1_logs', ConnectMySQL.engine, if_exists='append', index=False)
        
            df1_mysql = df_1_logs.to_csv("/app/df_1_logs.csv")       
            df1_mysql_q=pd.read_csv("/app/df_1_logs.csv")
 
            x=df1_mysql_q['id'].to_string(index=False).strip()
            y=df1_mysql_q['comments'].to_string(index=False).strip()


        class Merge:


            df2_mysql = pd.read_sql('select summary, description from data2 where id = \'{}\' '.format(Fields.x), 
                ConnectMySQL.engine).to_csv('df2_mysql_q_d.csv')
        
     
            dfdf=pd.read_csv('df2_mysql_q_d.csv')
            d11 = dfdf['summary'].to_string(index=False).strip()
            d22 = dfdf['description'].to_string(index=False).strip()
        
            df_comm3 = pd.DataFrame({"id": Fields.x, 
                                 "comments": Fields.y, 
                                 "summary" : d11 , 
                                 "description": d22 }, index=[0])


        class DfC3:
        
            Merge.df_comm3.to_csv("/app/df_comm3_single_logs.csv")
            Merge.df_comm3.to_sql('df_comm3_logs', ConnectMySQL.engine, if_exists='append', index=False)
            df_comm3_mysql=pd.read_sql('SELECT  * from df_comm3_logs ', ConnectMySQL.engine).to_csv("/app/df_comm3_logs.csv")


        class Compare:

            df_case_csv = pd.read_sql('SELECT * from df_case', ConnectMySQL.engine).to_csv("/app/df_case_logs.csv")
            df_comm3_csv_single_df = pd.read_csv('/app/df_comm3_single_logs.csv')
            df_case_csv_df = pd.read_csv('/app/df_case_logs.csv')

            is_it = df_case_csv_df.loc[df_case_csv_df['title']==df_comm3_csv_single_df['summary'][0]]

    
        if (Compare.is_it.shape[0] > 0):

            print("there is a case")

            class Case:
            
                extract_newdata_case_csv = pd.read_sql('SELECT * from new_data', ConnectMySQL.engine).to_csv('/app/new_data.csv')
                extract_case_csv = pd.read_sql('SELECT * from df_case', ConnectMySQL.engine).to_csv('/app/df_case.csv')
                extract_case_csv_df = pd.read_csv('/app/df_case.csv')
             

                extract_newdata_case_csv_d = pd.read_csv('/app/new_data.csv')

                title_case = Compare.df_comm3_csv_single_df['summary'].to_string(index=False).strip()

          
            class ID:

                find_case_id = Case.extract_case_csv_df.loc[Case.extract_case_csv_df['title'] == Compare.df_comm3_csv_single_df['summary'][0]].to_csv('/app/find_case_id.csv')

                find_case_id_csv_d = pd.read_csv('/app/find_case_id.csv')
                print("here is your bloody case ID")
                print(find_case_id_csv_d['id'][0])
                print("found case ID")
             
             
            class Task:

                print(Update.updated_comment)
                find_task_id = Case.extract_newdata_case_csv_d.loc[Case.extract_newdata_case_csv_d['id'] == ID.find_case_id_csv_d['id'][0]] 
                taskID_add_1=find_task_id['taskID'].to_string(index=False).strip()
                print("this is taskID")


            class Logs:

                json_log = {'message': '{}'.format(Update.updated_comment)  }
            
                print("http://{0}:9000/api/case/task/{1}/log".format(HostTheHive.hostname, Task.taskID_add_1))

                response_json_log = requests.post("http://{0}:9000/api/case/task/{1}/log".format(HostTheHive.hostname, Task.taskID_add_1),
                        auth=HTTPBasicAuth('{}'.format(UserTheHive.name), '{}'.format(PasswdTheHive.secret)), data=json_log)
                re11=response_json_log.json()
                print(re11)

     
        return jsonify({'new_comment': Update.updated_comment}), 201

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)

