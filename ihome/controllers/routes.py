#from flask import Blueprint, render_template, request
from flask import render_template
from ihome import app
#main = main_blueprint = Blueprint('main', __name__)

@app.route('/')
def index():
	return render_template('index.html')