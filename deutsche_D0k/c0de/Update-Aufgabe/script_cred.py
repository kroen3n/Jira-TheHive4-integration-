#!/usr/bin/python3


import os
import sys

from passwd import Encry


class UserDBA:
    name='root'

class UserTheHive:
    name='theuser'

class UserJira:
    name='artsy'


class PasswdTheHive:
    secret=Encry.pl

class PasswdDBA:
    secret=Encry.pl

class PasswdJira:
    secret=Encry.pl

class HostTheHive:
    hostname="172.17.0.5"


class HostJira:
    hostname="172.17.0.3"


class HostDBA:
    hostname="172.17.0.7"


class DBA:
    database="dataframes"
