from app import db



class Background(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
    type = db.Column(db.Integer)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

class Level(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    sizeX = db.Column(db.Integer)
    sizeY = db.Column(db.Integer)
    backgrounds = db.relationship('Background', backref = 'level', lazy = 'dynamic')