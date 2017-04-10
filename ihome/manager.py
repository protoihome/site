#!/usr/bin/python
# -*- coding: utf-8 -*-

from ihome import app, db
from controllers import routes

if __name__ == '__main__':
	db.create_all()
	db.session.commit()
	#app.run(host=Config.get_ip, port=Config.PORTA, debug=True, threaded=True)
	app.run(debug=True)
