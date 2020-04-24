from datetime import datetime
from chatapp import db, login_manager
from flask import app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    messages = db.relationship('ChatSchema', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class ChatSchema(db.Model):
    SID = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    time_sent = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Product('{self.message}', '{self.time_sent}')"
