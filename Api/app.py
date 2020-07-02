from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app,  db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
login = LoginManager(app)
login.login_view = 'login'


if __name__ == '__main__':
    manager.run()

import routes
from database import models

