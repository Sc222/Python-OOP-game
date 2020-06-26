from app import app, db
from database import models, models_DTO
from database.models_DTO import Background_Dto, LevelDto, Leaderboard_Dto
from flask import jsonify, g, make_response, request
from flask_login import current_user, login_required, login_user


@app.route('/leaderboard', methods=['GET'])
def Leaderboard():
    return jsonify([l.serialize() for l in models.LeaderboardRecord.query.all()])


@login_required
@app.route('/leaderboard/post', methods=['GET', 'POST'])
def PostLeaderboard_record():
    login = request.args.get('login')
    score = request.args.get('score')
    l = models.LeaderboardRecord(playerName=login, score=score)
    db.session.add(l)
    db.session.commit()
    response = make_response("zaebok", 200)


@app.route('/level/<id>', methods=['GET'])
def getLevel(id):
    dbLevel = models.Level.query.get(id)
    backgrounds_Dto = [Background_Dto(b.x, b.y, b.info.imageSource).__dict__ for b in dbLevel.backgrounds]
    return jsonify(LevelDto(backgrounds_Dto, [], []).__dict__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return make_response("zaebis", 200)
    login = request.args.get('login')
    password = request.args.get('password')
    login_user(models.User(nickname=login, password=password))
    return make_response(str(login), 200)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return make_response("zaebis", 200)
        login = request.args.get('login')
        password = request.args.get('password')
        user = models.User(login)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return make_response("ZAEBIS", 200)
