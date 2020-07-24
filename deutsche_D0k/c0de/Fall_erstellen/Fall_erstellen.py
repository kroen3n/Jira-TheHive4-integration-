#!/usr/bin/python3


# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

import os
from urllib.request import urlopen
import re
import pandas as pd
import json
from flask import request, jsonify
from requests.auth import HTTPBasicAuth
from pandas import json_normalize
import numpy as np
import subprocess

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


api = TheHiveApi('http://{}:9000'.format(HostTheHive.hostname), '***')
 
app=Flask(__name__)
tasks=[]

@app.route("/get/comments", methods=['POST'])


def hehe():


        class Update:
   
            up=request.data
            update_req = json.loads(up)
            df_updated=pd.DataFrame(update_req)

            print("new_comment from dataframe")
            updated_comment=df_updated['comment']['body']
            print(updated_comment)

         
        class Link:
         
            sel = Update.df_updated['comment']['self']
            url_sel = sel.split('/')
            new_url = sel.rsplit("/", 2)[0]
            #print(new_url) 
            updated_url = re.sub('localhost', '{}'.format(HostJira.hostname), new_url)

            
        class Extract:
         
            take_file = subprocess.call(["curl", "-u", 
                "{0}:{1}".format(UserJira.name, PasswdJira.secret), 
                "{}".format(Link.updated_url), "--output", 
                "/app/refactoring_code/new.json"], shell=False)

            read_file_js = pd.read_json('/app/refactoring_code/new.json')

        
        class Fields:

            data=[]
            da=[]

            da={'id': Extract.read_file_js['key']['assignee'], 'comments': Update.updated_comment}
            data.append(da)

            df_1=pd.DataFrame(data, columns=['id', 'comments'])      
            df_1.to_sql('df_1', ConnectMySQL.engine, if_exists='append', index=False)
     
            df1_mysql = df_1.to_csv("/app/refactoring_code/df_1.csv")
            df1_mysql_q=pd.read_csv("/app/refactoring_code/df_1.csv")
 
            x=df1_mysql_q['id'].to_string(index=False).strip()
            y=df1_mysql_q['comments'].to_string(index=False).strip()

   
        class Merge:

            df2_mysql = pd.read_sql('select summary, description from data2 where id = \'{}\''.format(Fields.x), 
                ConnectMySQL.engine).to_csv('df2_mysql_q_d.csv')

            print("merge")
            dfdf=pd.read_csv('df2_mysql_q_d.csv')
            d11 = dfdf['summary'].to_string(index=False).strip()
            d22 = dfdf['description'].to_string(index=False).strip()

            df_comm3=pd.DataFrame({"id": Fields.x, 
                               "comments" : Fields.y,
                               "summary" : d11,
                               "description": d22 }, index=[0])
        
        
        class DfC3:

            Merge.df_comm3.to_csv("/app/refactoring_code/df_comm3_single.csv")
            Merge.df_comm3.to_sql('df_comm3', ConnectMySQL.engine, if_exists='append', index=False)

            df_comm3_mysql=pd.read_sql('SELECT  * from df_comm3 ', ConnectMySQL.engine).to_csv("/app/refactoring_code/df_comm3.csv")

            
        class Compare:

            df_case_csv = pd.read_sql('SELECT * from df_case', ConnectMySQL.engine).to_csv("/app/refactoring_code/df_case.csv")
            df_comm3_csv_single_df = pd.read_csv('/app/refactoring_code/df_comm3_single.csv')
            df_case_csv_df = pd.read_csv('/app/refactoring_code/df_case.csv')
            
            is_it = df_case_csv_df.loc[df_case_csv_df['title']==df_comm3_csv_single_df['summary'][0]]
    

        if (Compare.is_it.shape[0] == 0):

            print("always create a case")

            class Title:

                extract_alert_csv = pd.read_sql('SELECT * from df_alert', ConnectMySQL.engine).to_csv('/app/df_alert.csv')
                print("convert to dataframe the df_alert csv")
                extract_alert_csv_df = pd.read_csv('/app/df_alert.csv')
                print(extract_alert_csv_df)
            
                title_case = Compare.df_comm3_csv_single_df['summary'].to_string(index=False).strip()
             
             
            class Alert:
            
                find_alert=Title.extract_alert_csv_df[Title.extract_alert_csv_df['title'] == Compare.df_comm3_csv_single_df['summary'][0]] 
                print(find_alert)

                print("here find the id")
                val21 = find_alert['id'].to_string(index=False).strip()
           

            class CreateCase: 

                response_create_case=requests.post("http://{0}:9000/api/alert/{1}/createCase".format(HostTheHive.hostname, Alert.val21),
                   auth=HTTPBasicAuth('{}'.format(UserTheHive.name), '{}'.format(PasswdTheHive.secret))

                print("response creation")
                print(response_create_case)
                data_create_case2=response_create_case.json()
                print(data_create_case2)
                id_case_readable2=data_create_case2['id']

                                                   
            class CreateTask:

                new_json_task2={'title': 'Jira comments'}

                response_create_new_task2=requests.post("http://{0}:9000/api/case/{1}/task".format(HostTheHive.hostname, 
                    CreateCase.id_case_readable2),
                    auth=HTTPBasicAuth('{}'.format(UserTheHive.name), '{}'.format(PasswdTheHive.secret)), 
                    data=new_json_task2)

                    
                new_repopo2=response_create_new_task2.json()
                new_df_task_id2=new_repopo2['id']

                didi22 = pd.DataFrame( { 'id':[CreateCase.id_case_readable2], 'taskID':[new_df_task_id2] } )
                didi22.to_sql('new_data', ConnectMySQL.engine, if_exists='append', index=False)


            class Logs:

                comix22 = Compare.df_comm3_csv_single_df['comments'].to_string(index=False).strip()
                json_log_new2={'message': '{}'.format(comix22)}

                response_json_log_new2 = requests.post("http://{0}:9000/api/case/task/{1}/log".format(HostTheHive.hostname, 
                    CreateTask.new_df_task_id2),
                  auth=HTTPBasicAuth('{}'.format(UserTheHive.name), '{}'.format(PasswdTheHive.secret)), data=json_log_new2)
                re112new=response_json_log_new2.json()

        #add new case to df_case
            class Addition:

                dfa=[]
                dfapp=[]

                dfa={"id": CreateCase.id_case_readable2, "title": Title.title_case }
                dfapp.append(dfa)

                df_app=pd.DataFrame(dfapp, columns=['id', 'title'])
                df_app.to_sql('df_case', ConnectMySQL.engine, if_exists='append', index=False)
                df_app.to_sql('df_case_logs', ConnectMySQL.engine, if_exists='append', index=False)

            
        else:
            print("case is already created")

                                                   
        return jsonify({'new_comment': Update.updated_comment}), 201
                                                   
                                                   
if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)


