from app import app, db
from database import models, models_DTO
from flask import jsonify
@app.route('/leaderboard',methods=['GET'])
def somedef():
    return jsonify([l.serialize() for l in models.LeaderboardRecord.query.all()])


