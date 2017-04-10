from ihome import db, app
from ihome import Config
from controllers import routes

if __name__ == '__main__':
	#db.create_all()

	#app.run(host=Config.get_ip, port=Config.PORTA, debug=True, threaded=True)
	app.run(debug=True)