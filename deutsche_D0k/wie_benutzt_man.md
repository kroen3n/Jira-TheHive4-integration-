<i> Wie benutzt man ... !!! [immer noch in Arbeit] !!! </i> 

<br></br>
>>Entwurfsmuster

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/envir.png)



Folgende Ports wurden den Flask-Diensten zugewiesen 

```
(base) root@kro3nen:/home/po0lt# # Flask1 für Aufgaben erstellen
(base) root@kro3nen:/home/po0lt# lsof -i :5002
COMMAND    PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
docker-pr 6267 root    4u  IPv6  57898      0t0  TCP *:rfe (LISTEN)
(base) root@kro3nen:/home/po0lt#
(base) root@kro3nen:/home/po0lt# # Flask2 für Kommentare
(base) root@kro3nen:/home/po0lt# lsof -i :5003
COMMAND     PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
docker-pr 19944 root    4u  IPv6 1759716      0t0  TCP *:5003 (LISTEN)
(base) root@kro3nen:/home/po0lt#
(base) root@kro3nen:/home/po0lt# # Flask3 für Kommentare hinzufügen
(base) root@kro3nen:/home/po0lt# lsof -i :5004
COMMAND     PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
docker-pr 15175 root    4u  IPv6 2806997      0t0  TCP *:5004 (LISTEN)

```

<br></br>
Die folgenden Webhooks wurden auf der Jira erstellt (jeder Webhook wird aus einem Flask-Dienst erstellt):

>>1. Aufgaben erstellen - 

<br></br>
![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/Aufgaben_erstellen.png)

>>2. Kommentare 

<br></br>
![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/Komentare.png)

>>3. Kommentare hinzufügen

<br></br>
![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/Kommentare_hinzufügen.png)


Die Datenbank kommuniziert nicht mit dem externen Netzwerk. 
Der MySQL-Container kommuniziert nur auf der Ebene des Docker Netzwerks.

```
(base) root@kro3nen:/home/po0lt# lsof -i :3306
(base) root@kro3nen:/home/po0lt#
```
<br></br>
<b> I) Jira-Ticket erstellen </b>

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/Erstes_Ticket_1.png)

<br></br>

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/Erstes_Ticket_2.png)



Flask Output:

Ausführen der Flask1-Webanwendung als Dienst (Port 5002 -  Aufgaben erstellen)
```
no attachment in ticket... creating alert with data...
[{'summary': 'Hallo, Welt!', 'description': 'Hallo, Welt!\xa0 Dies ist ein kleines Beispiel, das in Jira erstellt wurde.', 'id': 'SOC-23'}]
<Response [201]>
```

<br></br>
Alert erstellt in Hive4:

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/create_alert.png)

<br></br>

<b> II) Erster Kommentar </b>

Lassen Sie uns den ersten Kommentar in Jira hinzufügen: "Der erster Kommentar"

Ausführen der Flask2-Webanwendung als Dienst (Port 5003 - Kommentare)

```
response creation
<Response [201]>
{'_id': '1577168', 'id': '1577168', 'createdBy': 'theuser@thehive.local', 'updatedBy': None, 'createdAt': 1596558591070, 'updatedAt': None, '_type': 'case', 'caseId': 48, 'title': 'Hallo, Welt!', 'description': 'Hallo, Welt!\xa0 Dies ist ein kleines Beispiel, das in Jira erstellt wurde.', 'severity': 2, 'startDate': 1596558591054, 'endDate': None, 'impactStatus': None, 'resolutionStatus': None, 'tags': ['meh'], 'flag': False, 'tlp': 3, 'pap': 2, 'status': 'Open', 'summary': None, 'owner': 'theuser@thehive.local', 'customFields': {}, 'stats': {}, 'permissions': ['manageShare', 'manageAnalyse', 'manageTask', 'manageCaseTemplate', 'manageCase', 'manageUser', 'managePage', 'manageObservable', 'manageConfig', 'manageAlert', 'manageAction']}
create new task for new case id
        id    taskID
0  1577168  42664136

add logs to new task
172.17.0.3 - - [04/Aug/2020 16:29:51] "POST /get/comments?user_id=artsy&user_key=JIRAUSER10000 HTTP/1.1" 201 -

```
<br></br>

Die Warnung wird nun zum Fall:

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/Erster_Fall_1.png)

<br></br>
... Mit einer Aufgabe namens "Jira comments":


![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/Erster_Fall_2.png)


![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/Erster_Fall_3.png)

<br></br>

Die Aufgabe wird die Jira-Kommentare enthalten

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/Erster_Kommentar_Hive4.png)


<b> III) Kommentare hinzufügen </b>


Einen weiteren Kommentar hinzufügen in Jira:
<br></br>

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/Der_zweite_Kommentar_Jira.png)


Ausführen der Flask3-Webanwendung als Dienst (Port 5004 -- Kommentare hinzufügen)

```
here is case ID
1577168

Der zweite Kommentar

this is taskID
{'message': 'Der zweite Kommentar'}
http://172.17.0.5:9000/api/case/task/42664136/log
{'_id': '42676464', 'id': '42676464', 'createdBy': 'theuser@thehive.local', 'createdAt': 1596558750940, '_type': 'case_task_log', 'message': 'Der zweite Kommentar', 'startDate': 1596558750940, 'status': 'Ok', 'owner': 'theuser@thehive.local'}
172.17.0.3 - - [04/Aug/2020 16:32:30] "POST /update/comments?user_id=artsy&user_key=JIRAUSER10000 HTTP/1.1" 201 -
```

n.b: Wenn ein Kommentar unter einem bestehenden Fall hinzugefügt wird, bietet Flask2 eine Ausgabe an:
```
172.17.0.3 - - [04/Aug/2020 16:29:51] "POST /get/comments?user_id=artsy&user_key=JIRAUSER10000 HTTP/1.1" 201 -

Der zweite Kommentar
 
case is already created
172.17.0.3 - - [04/Aug/2020 16:32:30] "POST /get/comments?user_id=artsy&user_key=JIRAUSER10000 HTTP/1.1" 201 -
```

<br></br>
Jira Kommentar hinzugefügt in Hive4:

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/Der_zweite_Kommentar_Hive4.png)

