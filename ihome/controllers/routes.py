from flask import render_template, request, jsonify
from ihome.database.managedb import db
from ihome import app
from ihome.models.modelsDB import Devices,Rooms
from ihome.controllers.galileo import Device

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/devices',  methods=['POST', 'GET'])
def devices():
	if request.method == 'POST':
		dispositivos = []

		disp = Devices.query.filter_by(id_room= request.form['id']).all()
		comodo = Rooms.query.filter_by(id_= request.form['id']).all()
		#[{'comodo': 'Sala'}, {"aparelhos": [{"pin": 13, "id": 1, "nome": "Lampada 1", "status": 0}]}]
		for i in disp:

		#	if i.id_ == request.form['id']:
			dispositivos.append(dict(id=i.id_,name='{0} - [{1}]'.format(i.name,i.pin),status=i.status))
		# d = json.dumps(c, cls=AlchemyEncoder)
		return jsonify([{'comodo':c.__dict__.get('name') for c in comodo},{"aparelhos": dispositivos }])
	#return json.dumps(disp, cls=AlchemyEncoder)
        #return redirect(url_for('index'))
    #return jsonify(aparelhos=[dict(nome='teste',status=1,id=1),  dict(nome='teste2',status=0,id=2)])

##################################################################
###################Funcao para listar os comodos#############################

@app.route('/room')
def room():
    c = Rooms.query.all()
    comodos = []
    if c:
        for i in c:
            comodos.append(dict(id=i.id_,nome=i.name))
    return jsonify(comodos)
#######################################)#########################
##################Funcao para trocar o status do dispositivo#####################

@app.route('/swap',  methods=['POST', 'GET'])
def swap():

    if request.method == 'POST':

        #aparelho = request.form['id_ap']
        id_device = request.form['id']

        device = Devices.query.filter_by(id_ = id_device)
        status_device = request.form['estado']
        for i in device: pino = int(i.pin)
        home = Device(pino)
        if (status_device):

	        home.onDevice(pino)
        if (status_device == '0'):
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
