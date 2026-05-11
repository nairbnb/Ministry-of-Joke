from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True,
                         nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    jokes = db.relationship('Joke', backref='author',
                            lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Joke(db.Model):
    __tablename__ = 'joke'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.id}>'