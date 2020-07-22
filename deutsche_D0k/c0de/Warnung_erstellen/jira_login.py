#!/usr/bin/python3

import jira
import requests
from jira.client import JIRA
import json

from script_cred import HostJira
from script_cred import UserJira
from script_cred import PasswdJira


class JiraLogin:

    username=UserJira.name
    password=PasswdJira.secret

    jira=JIRA('http://{}:8080'.format(HostJira.hostname), basic_auth=(username, password))

    response = requests.get("http://{}:8080/rest/api/2/search?jql=project=SOC".format(HostJira.hostname), auth=(username, password))
    jj=response.json()


