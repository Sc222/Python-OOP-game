from app import app, db
from database import models, models_DTO
from database.models_DTO import Background_Dto,LevelDto,Leaderboard_Dto
from flask import jsonify
@app.route('/leaderboard',methods=['GET'])
def Leaderboard():
    return jsonify([l.serialize() for l in models.LeaderboardRecord.query.all()])

@app.route('/level/<id>',methods=['GET'])
def getLevel(id):
    dbLevel = models.Level.query.get(id)
    backgrounds_Dto = [Background_Dto(b.x,b.y,b.info.imageSource).__dict__ for b in dbLevel.backgrounds]
    return jsonify(LevelDto(backgrounds_Dto,[],[]).__dict__)