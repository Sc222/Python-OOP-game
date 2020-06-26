from flask_login import LoginManager

from app import app
app.run(debug=True) #todo add threaded and other
login_manager = LoginManager()
login_manager.init_app(app)

