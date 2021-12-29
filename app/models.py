from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120))
    avatar = db.Column(db.String(300), default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    reply = db.relationship('Reply', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(200),default=':)')

    def __repr__(self):
        return '<User {}>'.format(self.username)


    def user_avatar(self):
    #     imgmd5 = self.avatar.encode('utf-8')
        return '/static/avatar/{}'.format(self.avatar)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.password = self.password_hash

    def set_avatar(self, avatar_path):
        self.avatar = avatar_path

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
    tag = db.Column(db.Text, default='default')
    reply = db.relationship('Reply', backref='post', lazy='dynamic')

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pid = db.Column(db.Integer, db.ForeignKey('post.id'))


    def __repr__(self):
        return '<Reply {}>'.format(self.body)