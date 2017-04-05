#!/usr/bin/python
# -*- coding: utf-8 -*-

################ Bibliotecas utilizadas ##########################
import os, sqlite3, socket
from subprocess import Popen, PIPE
from classes import Home
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
###################################################################     
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)
####################################################################
####################################################################
##############################Classes importantes##########################

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

####################################################################
####################################################################
home = Home.Device(13)
#comodos = Banco.Rooms()
#dispositivos = Banco.Devices()
##################################################################
#########Funcao de render do template index###################################
@app.route('/index')
def index():
    return render_template('index.html')
##################################################################
#########Funcao para mandar o json para o aplicativo com os dispositivos###############

@app.route('/devices',  methods=['POST', 'GET'])
def devices():

	if request.method == 'POST':
      #aparelho = request.form['id_ap']
		id_ = int(request.form['id'])
		dicionario = {"aparelhos": [{"pin":7,"id": 3, "nome": "Lampada 3", "status":0}]}
	return jsonify(dicionario)	
        #return redirect(url_for('index'))
    #return jsonify(aparelhos=[dict(nome='teste',status=1,id=1),  dict(nome='teste2',status=0,id=2)])

##################################################################
###################Funcao para listar os comodos#############################

@app.route('/room')
def room():
	return jsonify(room=[dict(id=1,nome='sala'),  dict(id=2,nome='quarto')])

################################################################
##################Funcao para trocar o status do dispositivo#####################

@app.route('/swap',  methods=['POST', 'GET'])
def swap():

    if request.method == 'POST':
        #aparelho = request.form['id_ap']
        id_device = request.form['id']
        status_device = int(request.form['estado'])
        if (status_device):
            pino = 13
            home.onDevice(pino)


        if (status_device == 0):
            pino = 13
            home.offDevice(pino)


        #aqui entra a funcao para verificar o estado do pino na placa
        #return redirect(url_for('index'))
        return jsonify(status=status_device)

@app.route('/comodos')
def comdos():
	return render_template('comodos.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        comodos = Rooms(name=request.form['sala'])
        db.session.add(comodos)
        db.session.commit()
        dispositivos = Devices(name=request.form['dispositivo'],pin=request.form['pin'], device = comodos)
        db.session.add(dispositivos)
        db.session.commit()
    return render_template('add.html')

if __name__ == '__main__':
    #app.run(debug = True)
    #Comando para buscar informações e filtrar o ip
    db.create_all()
    db.session.commit()
    cmd = "ifconfig eth0 | grep 'inet addr:' | cut -d: -f2 | awk '{ print $1}'"
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    #Recebendo o IP que está na placa no eth0
    AdressIP, err = p.communicate()
    app.run(host=AdressIP, port=5000, debug=True,threaded=True)

