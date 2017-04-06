#!/usr/bin/python
# -*- coding: utf-8 -*-

################ Bibliotecas utilizadas ##########################
import os, sqlite3, socket,json
from subprocess import Popen, PIPE
from classes import Home
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy, DeclarativeMeta
from flask_sqlalchemy import DeclarativeMeta
###################################################################     
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ihome.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)
####################################################################
####################################################################
##############################Classes importantes##########################


class Rooms(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    addresses = db.relationship('Devices', backref='rooms', lazy='dynamic')

class Devices(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.String(50))
    name = db.Column(db.Integer)
    status = db.Column(db.Integer)
    id_room = db.Column(db.Integer, db.ForeignKey('rooms.id_'))

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
	    if isinstance(obj.__class__, DeclarativeMeta):
	        # an SQLAlchemy class
	        fields = {}
	        for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
	            data = obj.__getattribute__(field)
	            try:
	                json.dumps(data) # this will fail on non-encodable values, like other classes
	                fields[field] = data
	            except TypeError:
	                fields[field] = None
	        # a json-encodable dict
	        return fields

	    return json.JSONEncoder.default(self, obj)
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

	'''if request.method == 'POST':
		id_ = 1#int(request.form['id'])
        disp = Devices.query.filter_by(id_room = id_)

        #dicionario = {"aparelhos": [{"pin":disp['pin'],"id": disp['id'], "nome":disp['name'], "status":disp['']}]}
'''
	disp = Devices.query.all()
	return json.dumps(disp, cls=AlchemyEncoder)
        #return redirect(url_for('index'))
    #return jsonify(aparelhos=[dict(nome='teste',status=1,id=1),  dict(nome='teste2',status=0,id=2)])

##################################################################
###################Funcao para listar os comodos#############################

@app.route('/room')
def room():
    c = Rooms.query.all()
    return json.dumps(c, cls=AlchemyEncoder)
	#return jsonify(room=[dict(id=1,nome='sala'),  dict(id=2,nome='quarto')])

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
        dispositivos = Devices(name=request.form['dispositivo'],pin=request.form['pin'],status=0, rooms=comodos)
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

