from app import app, db
from database import models


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': models.User}