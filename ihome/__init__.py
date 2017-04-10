#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy


import os
from subprocess import Popen, PIPE

################ Bibliotecas utilizadas ##########################
#from .settings import Config
from flask import Flask

###################### CONFIGURAÇÕES #################################

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database/ihome.sqlite3')
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = "random string"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
DEBUG = True
PORTA = 5000
db = SQLAlchemy(app)

def get_ip(self):
	cmd = "ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"
	p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
	# Recebendo o IP que está na placa no eth0
	AdressIP, err = p.communicate()
	return AdressIP
