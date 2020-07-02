from app import db,login
from flask_login import UserMixin
import json
from werkzeug.security import generate_password_hash, check_password_hash


class Background(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    infoId = db.Column(db.Integer, db.ForeignKey('background_info.id'))
    info = db.relationship('BackgroundInfo', backref='background', lazy='select')


class BackgroundInfo(db.Model):
    __tablename__ = 'background_info'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,unique=True)
    db.UniqueConstraint('name', name='unique_component_commit')


class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sizeX = db.Column(db.Integer)
    sizeY = db.Column(db.Integer)
    backgrounds = db.relationship('Background', backref='level', lazy='dynamic')
    monsters = db.relationship('Monster', backref='level', lazy='dynamic')
    terrains = db.relationship('Terrain', backref='level', lazy='dynamic')


class MonsterInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
# путь до  папки со спрайтами (картинки будут храниться локально)
    # todo важно!!!(image будет отвечать за ПАПКУ, а в папке будут папки с анимациями attack, die, move и так далее)
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defence = db.Column(db.Integer)
    db.UniqueConstraint('name', name='unique_component_commit')


class Monster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    levelId = db.Column(db.Integer, db.ForeignKey('level.id'))
    infoId = db.Column(db.Integer, db.ForeignKey(MonsterInfo.id))
    info = db.relationship('MonsterInfo', backref='monster', lazy='select')
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nickname = db.Column(db.String,unique=True)
    password_hash = db.Column(db.String)  # хранится не пароль, а его хэш
    unlockedLevel = db.Column(db.Integer)  # максимальный разблок. уровень
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defence = db.Column(db.Integer)
    playerLevel = db.Column(db.Integer)
    xp = db.Column(db.Integer)
    db.UniqueConstraint('nickname',name='unique_component_commit')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return json.dumps({
            'nickname': self.nickname,
            'password': self.password,
            'hp': self.hp,
            'attack': self.attack,
            'defence': self.defence
        })

    def __init__(self, nickname):
        self.nickname = nickname
        self.unlockedLevel = 1
        self.hp = 100
        self.attack = 10
        self.defence = 50
        self.playerLevel = 1
        self.xp = 0

@login.user_loader
def load_user(id):
    print(id)
    return User.query.get(int(id))



class LeaderboardRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    playerName = db.Column(db.String)
    levelId = db.Column(db.Integer)
    score = db.Column(db.Integer)

    def serialize(self):
        return {'id': self.id,
                'playerName': self.playerName,
                'levelId': self.levelId,
                'score': self.score
                }


class TerrainInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    db.UniqueConstraint('name', name='unique_component_commit')



class Terrain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    levelId = db.Column(db.Integer, db.ForeignKey('level.id'))
    infoId = db.Column(db.Integer, db.ForeignKey(TerrainInfo.id))
    info = db.relationship('TerrainInfo', backref='terrain', lazy='select')
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
