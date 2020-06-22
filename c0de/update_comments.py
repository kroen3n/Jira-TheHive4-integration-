import jira
import requests
import pandas as pd
from jira.client import JIRA
import json
from flask import request, jsonify
from requests.auth import HTTPBasicAuth
from pandas import json_normalize
import numpy as np

from flask import Flask

import requests
import sys
import time
import uuid
from thehive4py.api import TheHiveApi
from thehive4py.models import Alert, AlertArtifact, CustomFieldHelper


# access to TheHive4

api = TheHiveApi('http://172.17.0.5:9000', '***')

# access to Jira

username="artsy"
password="***"
jira=JIRA('http://172.17.0.3:8080', basic_auth=(username, password))
response = requests.get("http://172.17.0.3:8080/rest/api/2/search?jql=project=SOC", auth=(username, password))
jj=response.json()

 
app=Flask(__name__)


@app.route("/get/comments", methods=['POST'])

def hehe():
    update_req=request.get_json()
    df_updated=pd.DataFrame(update_req)
    print("new_comment from dataframe")
    updated_comment=df_updated['comment']['body']
    print(df_updated['comment']['body'])
    print(df_updated['comment']['id'])

    data=[]
    da=[]
    
    open_issue=jira.search_issues('project=SOC and comment !~ \"honhon\"',
                              fields='comment', json_result=True)
                              
    df1=pd.DataFrame(open_issue)
    for i in range(df1.shape[0]):
        for j in range(0, len(df1['issues'][i]['fields']['comment']['comments'])):
            comments=df1['issues'][i]['fields']['comment']['comments'][j]['body']
            identity=df1['issues'][i]['key']

            da={'identity': identity, 'comments': comments}
            data.append(da)

    df_1=pd.DataFrame(data, columns=['identity', 'comments'])
    print(df_1)


    data2=[]
    da2=[]
    
    for i in range(jj['total']):
        df = pd.DataFrame(jj['issues'][i])
        summary = df['fields']['summary']
        description = df['fields']['description']
        identity1 = df['key'][i]

        da2={"summary" : summary, "description" : description, "identity" : identity1}
        data2.append(da2)


    df_2=pd.DataFrame(data2, columns=['summary', 'description', 'identity'])
    df_3 = pd.merge(df_1, df_2, how='inner')

    co3=[]
    comm3=[]

    for i in range(df_3.shape[0]):

        comments_=df_3['comments'][i]
        identity_=df_3['identity'][i]
        summary_=df_3['summary'][i]

        if(df_3['comments'][i] == df_updated['comment']['body']):
           co3={'identity': identity_, 'comments': comments_, 'summary': summary_}
           comm3.append(co3)

    df_comm3 = pd.DataFrame(comm3, columns=['identity', 'comments', 'summary'])
    print(" ")
    print("df_cmm3")
    print(df_comm3)
    print(" ")

    co4=[]
    comm4=[]
    
    this_value=df_comm3['summary'][0]

    url_case="http://172.17.0.5:9000/api/case/"
    response_hive4_case = requests.get(url_case, auth=HTTPBasicAuth('theuser', '***'))
    data_hive4_case = response_hive4_case.json()
    data_normalize_case = json_normalize(data=data_hive4_case)

    
    if(data_normalize_case.shape[0]==0):
        print("there are no cases...")
    else:
        print("getting data from new cases")
        data21=data_normalize_case[['id', 'title']]
        df_case=pd.DataFrame(data21)
        print("df_case")
        print(df_case)

    ## dataframe throws errors 
    ## if no alert created on TheHive4 side

    url_alert="http://172.17.0.5:9000/api/alert/"
    response_hive4_alert = requests.get( url_alert, auth=HTTPBasicAuth('theuser', '***'))
    data_hive4_alert=response_hive4_alert.json()
    
    data_normalize_alert=json_normalize(data=data_hive4_alert)
    print("data normalize alert from hive4")
    print(data_normalize_alert)
    
    #in case nothing created in systems
    if(data_normalize_alert.shape[0]==0):
        print("make sure there is an alert created on TheHive4")
    else:
        data22=data_normalize_alert[['id', 'title']]
        df_alert = pd.DataFrame(data22)
        print("df_alert -- dataframe from normalize hive4")
        print(df_alert)
 
    if(data_normalize_case.shape[0]==0 and data_normalize_alert.shape[0]==0):
        print("data not yet created")

    if(data_normalize_case.shape[0]==0 and data_normalize_alert.shape[0]>0):
        print("no cases, but alerts created")
        ale_df=df_alert.loc[df_alert['title']==df_comm3['summary'][0]]
        print(ale_df)
        if(ale_df.shape[0]>0):
            print("create case for alert here")
            value=ale_df['id']
            val=value.to_string(index=False)
            val1=val.strip()
            print("val1 ID  from ale_df")
            print(val1)

            response_create_case=requests.post("http://172.17.0.5:9000/api/alert/{}/createCase".format(val1),
                    auth=HTTPBasicAuth('theuser', '***'))
                    
            data_create_case=response_create_case.json()
            #print(data_create_case)
            id_case_readable=data_create_case['id']
            #print("/opt/{}".format(id_case_readable))
            print("create new task for id")

            new_json_task={'title': 'Jira comments'}
            response_create_new_task=requests.post("http://172.17.0.5:9000/api/case/{}/task".format(id_case_readable), 
                    auth=HTTPBasicAuth('theuser', '***'), data=new_json_task)

            new_repopo=response_create_new_task.json()

            new_df_task_id=new_repopo['id']
            print("/opt/{}".format(new_df_task_id))

            #here to create temporary table
         
            didi = pd.DataFrame({'id':[id_case_readable], 'taskID':[new_df_task_id]})
            #print(didi)
            didi.to_csv(r'/home/lmao.csv', mode='a', index=False, header=False)


            print("add logs to new task")
            comix=(df_comm3['comments']).to_string(index=False).strip()
            json_log_new={'message': '{}'.format(comix)}
            
            response_json_log_new = requests.post("http://172.17.0.5:9000/api/case/task/{}/log".format(new_df_task_id), 
                    auth=HTTPBasicAuth('theuser', '***'), data=json_log_new)
            re111new=response_json_log_new.json()
            print(re111new)

    if(data_normalize_case.shape[0]>0 and data_normalize_alert.shape[0]>0):
        ale_df3=df_case.loc[df_case['title']==df_comm3['summary'][0]]
        print("cases and alerts created")

        if(ale_df3.shape[0]>0):
            print("we have an alert with a case")
            print("check in temporary table if case ID coresponding to alert ID has a task ID")
            #print("for alert ID " + df_alert['id'] + "there is case ID " + df_case['id'])
            print("case ID for which I search")
       
            caseID_program=ale_df3['id'].to_string(index=False).strip()
            print(type(caseID_program))
            
            int_id = int(caseID_program)

            read_temporary_data = pd.read_csv('/home/lmao.csv')


            #checks temporary data until finding the required id, int_id
            
            dsds = read_temporary_data[(read_temporary_data.id == int_id  )]
            taskID_add = dsds['taskID']
            taskID_add_1 = taskID_add.to_string(index=False).strip()
                
            print("...... adding jira comment as log...")
            
            comix = (df_comm3['comments']).to_string(index=False).strip()
            json_log = {'message': '{}'.format(comix)  }
            response_json_log = requests.post("http://172.17.0.5:9000/api/case/task/{}/log".format(taskID_add_1),
                        auth=HTTPBasicAuth('theuser', '***'), 
                        data=json_log)
                        
            re11=response_json_log.json()
            print(re11)

        else:
            print("there is no case created for this alert")
            print("creating case for alert")
            ale_df2=df_alert.loc[df_alert['title']==df_comm3['summary'][0]]
            print("ale_df2")
            print(ale_df2)
            if(ale_df2.shape[0]==0):
                print("stop here...")
            if(ale_df2.shape[0]>0):
                value=ale_df2['id']
                val2=value.to_string(index=False)
                val21=val2.strip()
                print("val1 ID  from ale_df")
                print(val21)

                response_create_case=requests.post("http://172.17.0.5:9000/api/alert/{}/createCase".format(val21),
                    auth=HTTPBasicAuth('theuser', '***'))
                #print("response creation")
                #print(response_create_case)
                data_create_case2=response_create_case.json()
                #print(data_create_case2)
                id_case_readable2=data_create_case2['id']

                print("create new _Jira comments_ task for new case id")

                new_json_task2={'title': 'Jira comments'}
                response_create_new_task2=requests.post("http://172.17.0.5:9000/api/case/{}/task".format(id_case_readable2),
                    auth=HTTPBasicAuth('theuser', '***'), data=new_json_task2)

                new_repopo2=response_create_new_task2.json()
                new_df_task_id2=new_repopo2['id']

                #here to create temporary table

                didi22 = pd.DataFrame({'id':[id_case_readable2], 'taskID':[new_df_task_id2]})
                didi22.to_csv(r'/home/lmao.csv', mode='a', index=False, header=False)

                print("add logs to new task")
                
                comix22=(df_comm3['comments']).to_string(index=False).strip()
                json_log_new2={'message': '{}'.format(comix22)}

                response_json_log_new2 = requests.post("http://172.17.0.5:9000/api/case/task/{}/log".format(new_df_task_id2),
                    auth=HTTPBasicAuth('theuser', '***'), 
                    data=json_log_new2)
                    
                re112new=response_json_log_new2.json()
                
                print(re112new)


    return jsonify({'new_comment': updated_comment}), 201


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)
