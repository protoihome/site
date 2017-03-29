# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)
####################################################################
####################################################################
####################################################################


# Load default config and override config from an environment variable
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

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
##################################################################
#########Funcao de render do template index###################################
@app.route('/index')
def index():
    return render_template('index.html')
##################################################################
#########Funcao para inserir dados no banco####################################
@app.route('/add_room', methods=['POST'])
def add_rooms():
    #if not session.get('logged_in'):
       # abort(401)
    db = get_db()
    db.execute('insert into rooms (name, descricao) values (?, ?)',
                 [request.form['room'], request.form['description']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('index'))

##################################################################
#########Funcao de teste para retornar os dados do banco############################
@app.route('/show_room')
def show_rooms():
    db = get_db()
    cur = db.execute('select name, descricao from room order by id desc')
    room = cur.fetchall()
    return render_template('show_rooms.html', room=room)


if __name__ == '__main__':
    app.run(debug = True)
