#!/usr/bin/python
# -*- coding: utf-8 -*-
from ihome.controllers.galileo import Dicionario
from ihome import db
class Devices(db.Model):

    id_ = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.Integer, unique=True)
    name = db.Column(db.Integer)
    status = db.Column(db.Integer)
    id_room = db.Column(db.Integer, db.ForeignKey('rooms.id_'))


class Rooms(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    addresses = db.relationship('Devices', backref='rooms', lazy='dynamic')


