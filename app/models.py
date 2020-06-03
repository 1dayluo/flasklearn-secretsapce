from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120))
    avatar = db.Column(db.String(120))
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # def is_authenticated(self):
    #     return True
    # def is_active(self):
    #     return True
    # def is_anonymous(self):
    #     return False
    def avatar(self, imgmd5):
        imgmd5 = self.avatar.encode('utf-8')
        return './static/avatar/{}'.format(imgmd5)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.password = self.password_hash

    def check_password(self, password):
        return check_password_hash(self.password, generate_password_hash(password))

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.Column(db.Text)


    def __repr__(self):
        return '<Post {}>'.format(self.body)

