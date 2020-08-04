<i> Wie benutzt man </i>

<br></br>
Entwurfsmuster

![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/envir.png)



Folgende Ports wurden den Flask-Diensten zugewiesen 

```
(base) root@kro3nen:/home/po0lt# lsof -i :5002
COMMAND    PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
docker-pr 6267 root    4u  IPv6  57898      0t0  TCP *:rfe (LISTEN)
(base) root@kro3nen:/home/po0lt# lsof -i :5003
COMMAND     PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
docker-pr 19944 root    4u  IPv6 1759716      0t0  TCP *:5003 (LISTEN)
(base) root@kro3nen:/home/po0lt# lsof -i :5004
COMMAND     PID USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
docker-pr 15175 root    4u  IPv6 2806997      0t0  TCP *:5004 (LISTEN)

```

<br></br>
Die folgenden Webhooks wurden auf der Jira erstellt (jeder Webhook wird aus einem Flask-Dienst erstellt):

>>1. Aufgaben erstellen

<br></br>
![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/Aufgaben_erstellen.png)

>>2. Komentare 

<br></br>
![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/Komentare.png)

>>3. Kommentare hinzufügen

<br></br>
![alt text](https://raw.githubusercontent.com/kroen3n/Jira-TheHive4-integration-/master/deutsche_D0k/pics/Kommentare_hinzufügen.png)


Der Datenbank Port wurde nicht offengelegt:

```
(base) root@kro3nen:/home/po0lt# lsof -i :3306
(base) root@kro3nen:/home/po0lt#
```


