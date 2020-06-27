from app import app, db
from database import models
import  json
from database.models_DTO import Background_Dto, LevelDto, Terrain_Dto, User_Dto
from flask import jsonify, make_response, request
from flask_login import current_user, login_required, login_user


@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    level = request.args.get('level')
    if level is None:
        return make_response("Level is not specified", 400)

    leaderboard_records = models.LeaderboardRecord.query \
        .filter_by(levelId=level) \
        .order_by(models.LeaderboardRecord.score.desc())
    return jsonify([l.serialize() for l in leaderboard_records])


# @login_required
@app.route('/leaderboard/post', methods=['GET', 'POST'])
@login_required
def post_leaderboard_record():
    score = request.args.get('score')
    level = request.args.get('level')
    if score is None:
        return make_response("Score is not specified", 400)
    if level is None:
        return make_response("Level is not specified", 400)
    u = current_user
    leaderboard_record = models.LeaderboardRecord.query.filter_by(playerName=u.nickname, levelId=level).first()
    if leaderboard_record is None:  # Добавление нового рекорда
        l = models.LeaderboardRecord(playerName=u.nickname, score=score, levelId=level)
        db.session.add(l)
        response_text = "added new leaderboard record"
    else:  # Обновление существующего рекорда
        leaderboard_record.score = score
        response_text = "updated leaderboard record"
    db.session.commit()
    response = make_response(response_text, 200)
    return response


@app.route('/user', methods=['GET'])
@login_required
def get_user():
    # u = models.User.query.filter_by(nickname=name).first()
    # if u is None:
    #     return jsonify({"error":"user does not exist"})
    u = current_user
    user_dto = [User_Dto(u.nickname, u.unlockedLevel, u.hp, u.attack,u.defence,u.playerLevel,u.xp).__dict__ ]
    return jsonify(user_dto)


@app.route('/level/<id>', methods=['GET'])
def get_level(id):
    db_level = models.Level.query.get(int(id))

    print(id)
    print(db_level)

    backgrounds_dto = [Background_Dto(b.x, b.y, b.info.name).__dict__ for b in db_level.backgrounds]
    terrains_dto = [Terrain_Dto(t.x, t.y, t.info.name).__dict__ for t in db_level.terrains]
    return jsonify(LevelDto(backgrounds=backgrounds_dto,terrains=terrains_dto,monsters=[]).__dict__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return make_response("User is already logged in", 200)

    login = request.args.get('login')
    password = request.form.get('password')
    if login is None:
        return make_response("Login is not specified", 400)
    if password is None:
        return make_response("Password is not specified", 400)
    u = models.User.query.filter_by(nickname=login).first()

    if u is None:
        return make_response('User is not registered', 400)

    if u.check_password(password):
        login_user(u)
    else:
        return make_response('Incorrect password', 400)
    return make_response("Logged in successfully as " + login, 200)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return make_response("User is already registered and logged in", 200)
    login = request.args.get('login')
    password = request.form.get('password')

    if models.User.query.filter_by(nickname=login).first() is not None:
        return make_response("User is already registered", 400)
    user = models.User(login)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return make_response("User registered", 200)
