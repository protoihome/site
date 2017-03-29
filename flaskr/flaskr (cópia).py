# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
app = Flask(__name__)
#####################################################################
dados = {}
#####################################################################

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'ihome.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

##############funcoes de conexao com o banco de dados##########################
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


##################################################################
###################funcao para criar o banco de dados##########################
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
#################################################################
##############funcao para listar os dados no banco de dados#######################
@app.route('/')
def show_rooms():
    db = get_db()
    cur = db.execute('select name, descricao from rooms order by id desc')
    rooms = cur.fetchall()
    return render_template('show_rooms.html', rooms=rooms)

#@app.route('/')
#def index():
    #return render_template('index.html')

####################################################################
#funcao para receber os dados da pegina de metodo post
@app.route('/env',methods = ['POST', 'GET'])
def env():
    if request.method == 'POST':
        env = request.form #adicionando os dados recebidos na variavel env

        ################aqui entra a funcao de calculo de ip###############################

        ip = request.form['numIP']
        lensm = request.form['numSM']

        calculo = CalculoIp(lensm)

        a = calculo.getIP(ip)  # colocar a variavel com IP para calcular e verificar o tipo
        dados['IP Address'] = calculo.toDec(a)

        b = calculo.getSM(lensm) #armazena a sub mascara
        dados['Sub-Mask Address'] = calculo.toDec(b)

        c = calculo.getIpRede(a,b)
        dados['Network Address'] = calculo.toDec(c)

        reversoSM = calculo.reversSM(b,c)
        d = reversoSM

        e = calculo.getBroadcast(a,c,d)
        dados['Broadcast Address'] = calculo.toDec(e)

        dados['Hosts'] = calculo.getHST(b)

        ########################################################################################################################

        return render_template("dados.html",env = dados) #renderizando a pagina com os dados calculados


if __name__ == '__main__':
    app.run(debug = True)
