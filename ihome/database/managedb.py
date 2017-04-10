from ihome import create_db
app = create_db()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)