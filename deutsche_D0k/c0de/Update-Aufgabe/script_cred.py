#!/usr/bin/python3


import os
import sys


class UserDBA:
    name='root'

class UserTheHive:
    name='theuser'

class UserJira:
    name='artsy'


class PasswdTheHive:
    secret='***'

class PasswdDBA:
    secret='***'

class PasswdJira:
    secret='***'

class HostTheHive:
    hostname="172.17.0.5"


class HostJira:
    hostname="172.17.0.3"


class HostDBA:
    hostname="172.17.0.7"


class DBA:
    database="dataframes"
