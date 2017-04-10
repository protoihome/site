#!/usr/bin/python
# -*- coding: utf-8 -*-

################ Bibliotecas utilizadas ##########################
from .settings import Config
from flask import Flask

def create_db():
	app = Flask(__name__)
	app.config.from_object(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
	app.config['SECRET_KEY'] = "random string"
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
	return app
app = create_db()
