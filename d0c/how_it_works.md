
<i> A step-by-step tutorial will be done under the German documentation folder, 
       including the automation part (in code) for building up the entire environment on containers </i>


Flask services running on following ports:


```
root@kroen3n:/home/poke# lsof -i :5003
COMMAND     PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
docker-pr 19944 root    4u  IPv6 1759716      0t0  TCP *:5003 (LISTEN)

root@kroen3n:/home/poke#
COMMAND    PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
docker-pr 6267 root    4u  IPv6  57898      0t0  TCP *:rfe (LISTEN)
root@dante-ThinkPad-X260:/home/poke/app/pandy/mumu# 
```

i) Flask service 1

- generated by c0de/create_withorwithout_attachment.py 
- new alerts creation (with or without attachments),  
- running on port 5002
- with route /created/task

In Jira, webhook for service Flask 1 will be setup as following:

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/pics/webhook_new_alert.png)



ii) Flask service 2

- generated by c0de/update_comments.py
- comments replication
- running on port 5003
- with route /get/comments

In Jira, webhook for service Flask 2 will be setup as following:

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/pics/webhook_comments.png)


<b> Case scenarios</b></br>

1) Create Alert without attachment in Jira - you should see replication in TheHive4

- On Jira side, ticket creation

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/pics/wtf.png)

- On TheHive4 side, data replication in an alert

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/pics/alert_thehive4_without_attachment.png)


and the preview of newly created alert
![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/pics/alert_without_attachment_preview.png)


</br>

2) Create Alert with attachment in Jira - you should see data replication in TheHive4

- On Jira side, ticket creation with attachment

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/pics/jira_alert_with_attachment.png)

- On TheHive4 side, data replication in the alert
![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/pics/thehive4_with_attachment.png)

and the alert preview, along with the file attachment
![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/pics/thehive4_attachment_preview.png) 


3) Comments replication  -- this only happens if existing alerts in TheHive4 have been replicated from Jira tickets

- add Jira comment in previously created ticket (the one with machine learning meme attachment)
![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/pics/1st.png)

- On TheHive4 side, alert is turned into case. 
![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/pics/alert_turns_to_case.png)

The Jira comments are stored under "Jira comments" task, as logs:

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/pics/created_task.png)

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/pics/task_1st_log.png)


What you see in Flask logs when turning alert into case, and adding first log to "Jira comments" task:
```
response creation
<Response [201]>
{'_id': '200944', 'id': '200944', 'createdBy': 'theuser@thehive.local', 'updatedBy': None, 'createdAt': 1593019696476, 'updatedAt': None, '_type': 'case', 'caseId': 9, 'title': 'alert with attachment', 'description': 'description for alert with attachment', 'severity': 2, 'startDate': 1593019696473, 'endDate': None, 'impactStatus': None, 'resolutionStatus': None, 'tags': ['lelol'], 'flag': False, 'tlp': 3, 'pap': 2, 'status': 'Open', 'summary': None, 'owner': 'theuser@thehive.local', 'customFields': {}, 'stats': {}, 'permissions': ['manageShare', 'manageAnalyse', 'manageTask', 'manageCaseTemplate', 'manageCase', 'manageUser', 'managePage', 'manageObservable', 'manageConfig', 'manageAlert', 'manageAction']}
create new task for new case id
       id    taskID
0  200944  82149472
add logs to new task
{'_id': '41410584', 'id': '41410584', 'createdBy': 'theuser@thehive.local', 'createdAt': 1593019696754, '_type': 'case_task_log', 'message': 'k0mmentz about ML', 'startDate': 1593019696754, 'status': 'Ok', 'owner': 'theuser@thehive.local'}
```

Add another comment in Jira ticket
![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/pics/2nd.png)


On TheHive4 side:

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/pics/task_2ndlog.png)

What you should see in Flask logs when adding another comment into Jira (comment to be replicated into TheHive4 as another task log):

```
we have an alert with a case
check in temporary table if case ID coresponding to alert ID has a task ID

read table
         id    taskID
0  82120784  41275416
1  82112608  82116704
2  41156840  41283752
3    200944  82149472

...... adding jira comment as log...

{'_id': '41316520', 'id': '41316520', 'createdBy': 'theuser@thehive.local', 'createdAt': 1593019865691, '_type': 'case_task_log', 'message': 'another comment about ML memes', 'startDate': 1593019865691, 'status': 'Ok', 'owner': 'theuser@thehive.local'}
172.17.0.3 - - [24/Jun/2020 17:31:05] "POST /get/comments?user_id=artsy&user_key=JIRAUSER10000 HTTP/1.1" 201 -
```

Temporary table is created from a csv file. All new entries (case ID and task ID) are saved here ...  (from here on, python dataframes are applied).
```
root@flasck2:/app# more /home/lmao.csv 
id,taskID
82120784,41275416
82112608,82116704
41156840,41283752
200944,82149472
root@flaskc2:/app# 
```


