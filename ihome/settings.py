#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from subprocess import Popen, PIPE


basedir = os.path.abspath(os.path.dirname(__file__))


###################### CONFIGURAÇÕES #################################
class Config(object):

	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite://' + os.path.join(basedir, 'database/ihome.sqlite')
	PORTA = 5000
	def get_ip(self):
		cmd = "ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"
		p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
		# Recebendo o IP que está na placa no eth0
		AdressIP, err = p.communicate()
		return AdressIP