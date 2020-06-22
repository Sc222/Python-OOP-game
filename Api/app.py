from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


if __name__ == '__main__':
    app.run(debug=True)

import routes
from database import models



