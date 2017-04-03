#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class Rooms(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	addresses = db.relationship('Devices', backref='device', lazy='dynamic')

class Devices(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	pin = db.Column(db.String(50))
	name = db.Column(db.Integer)
	status = db.Column(db.String(30))
	id_room = db.Column(db.Integer, db.ForeignKey('device.id'))