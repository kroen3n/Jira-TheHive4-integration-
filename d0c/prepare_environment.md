<i>How to build everything on containers (quick indications)</i>


TheHive4 needs systemd - you'll need to access that from a container

Cassandra and HDFS have several Docker images available. If you go with HDFS and not local filesystem, make sure you change the port 9000.

Flask service can be easily ported to docker containers.

The Jira attlassian docker image I have used: https://github.com/cptactionhank/docker-atlassian-jira

This environment on containers look as following:
```
2 flask service containers (172.17.0.2, respectively 172.17.0.6)
1 Cassandra container (172.17.0.4)
1 TheHive4 container, on which systemd runs (172.17.0.5)
1 Jira container (172.17.0.3)
```


>> A step-by-step tutorial will be done under the German documentation folder, 
including the automation part in code for building up the entire environment on containers


