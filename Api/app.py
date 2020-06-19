from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)



from database import  models
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return [];

if __name__ == '__main__':
    app.run(debug=True)