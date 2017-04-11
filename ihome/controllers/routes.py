#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify
from ihome import app,db
from ihome.models.modelsDB import Devices,Rooms
from ihome.controllers.galileo import InDevices, Dicionario

@app.route('/')
def main():

	return render_template('index.html')

@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/devices',  methods=['POST', 'GET'])
def devices():
	if request.method == 'POST':
		dispositivos = []
		disp = Devices.query.filter_by(id_room= request.form['id']).all()
		comodo = Rooms.query.filter_by(id_= request.form['id']).all()
		for i in disp:
			dispositivos.append(dict(id=i.id_,name='{0} - [{1}]'.format(i.name,i.pin),status=i.status))
		return jsonify([{'comodo':c.__dict__.get('name') for c in comodo},{"aparelhos": dispositivos }])

#########################   Funcao para listar os comodos   #############################

@app.route('/room')
def room():
	#a variavel 'c' armazena a consulta no BD
	c = Rooms.query.all()
	comodos = []
	if c:
		for i in c:
			comodos.append(dict(id=i.id_, nome=i.name))
	return jsonify(comodos)

########################## Funcao para trocar o status do dispositivo#####################

@app.route('/swap',  methods=['POST', 'GET'])
def swap():

    if request.method == 'POST':

        id_device = request.form['id']

        device = Devices.query.filter_by(id_ = id_device)
        status_device = request.form['estado']

        for i in device:
	        pino = int(i.pin)

        if (status_device == '0'):
            InDevices.offDevice(pino)
            for i in device:
                i.status = status_device
                status = i.status
                db.session.commit()
        else:
	        InDevices.onDevice(pino)
	        for i in device:
		        i.status = status_device
		        status = i.status
		        db.session.commit()


        #aqui entra a funcao para verificar o estado do pino na placa
        #return redirect(url_for('index'))
        return jsonify(status=status)

@app.route('/comodos')
def comodos():
	return render_template('comodos.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/add_device', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        dispositivos = Devices(name=request.form['dispositivo'],pin=request.form['pin'],status=0, id_room=request.form['cm'])
        db.session.add(dispositivos)
        db.session.commit()
    return render_template('add_device.html', comodo = Rooms.query.all())

@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
	if request.method == 'POST':
		comodos = Rooms(name=request.form['comodo'])
		db.session.add(comodos)
		db.session.commit()
	return render_template('add_room.html')

@app.cli.command('initpin')
def setPins():
	dispositivos = Devices.query.all()
	if dispositivos:
		for dispositivo in dispositivos:
			InDevices(dispositivo.pin)
			if dispositivo.status == 0:
				InDevices.offDevice(dispositivo.pin)
			else:
				InDevices.onDevice(dispositivo.pin)