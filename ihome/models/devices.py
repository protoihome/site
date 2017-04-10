from ihome import db

class Devices(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.Integer)
    name = db.Column(db.Integer)
    status = db.Column(db.Integer)
    id_room = db.Column(db.Integer, db.ForeignKey('rooms.id_'))
