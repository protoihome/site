#!/usr/bin/python
# -*- coding: utf-8 -*-

from ihome import app, db, get_ip, PORTA
from controllers import routes

if __name__ == '__main__':
	db.create_all()
	db.session.commit()
	host = get_ip()
	#app.run(host=Config.get_ip, port=Config.PORTA, debug=True, threaded=True)
	app.run(host=host, port=PORTA, debug=True, threaded=True)
