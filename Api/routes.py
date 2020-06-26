from app import app, db
from database import models, models_DTO
from database.models_DTO import Background_Dto, LevelDto, Leaderboard_Dto
from flask import jsonify, g, make_response, request
from flask_login import current_user, login_required, login_user


@app.route('/leaderboard', methods=['GET'])
def Get_Leaderboard():
    level = request.args.get('level')
    if level is None:
        return make_response("Level is not specified", 400)

    leaderboard_records = models.LeaderboardRecord.query \
        .filter_by(levelId=level) \
        .order_by(models.LeaderboardRecord.score.desc())
    return jsonify([l.serialize() for l in leaderboard_records])


@app.route('/leaderboard/post', methods=['GET', 'POST'])
@login_required
def PostLeaderboard_record():
    login = request.args.get('login')
    score = request.args.get('score')
    level = request.args.get('level')
    if login is None:
        return make_response("Login is not specified", 400)
    if score is None:
        return make_response("Score is not specified", 400)
    if level is None:
        return make_response("Level is not specified", 400)

    leaderboard_record = models.LeaderboardRecord.query.filter_by(playerName=login, levelId=level).first()
    if leaderboard_record is None:  # Добавление нового рекорда
        l = models.LeaderboardRecord(playerName=login, score=score, levelId=level)
        db.session.add(l)
        response_text = "added new leaderboard record"
    else:  # Обновление существующего рекорда
        leaderboard_record.score = score
        response_text = "updated leaderboard record"
    db.session.commit()
    response = make_response(response_text, 200)
    return response


@app.route('/level/<id>', methods=['GET'])
def getLevel(id):
    dbLevel = models.Level.query.get(id)
    backgrounds_Dto = [Background_Dto(b.x, b.y, b.info.imageSource).__dict__ for b in dbLevel.backgrounds]
    return jsonify(LevelDto(backgrounds_Dto, [], []).__dict__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return make_response("You are already logged in", 200)
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
        login_user(models.User(nickname=login))
    else:
        return make_response('Incorrect password', 400)
    return make_response("Logged in successfully: " + str(login) + str(password), 200)


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
