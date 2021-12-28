from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import  LoginManager
from markdown import Markdown
from flaskext.markdown import Markdown

app = Flask(__name__)
app.config.from_object(Config)
Markdown(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.debug = True

login = LoginManager(app)
login.login_view = 'login'
@app.before_first_request
def create_tables():
    db.create_all()
from app import routes, models
