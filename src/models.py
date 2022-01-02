from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
import random

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

    bookmarks = db.relationship("Bookmark", backref="user", lazy=True)

    def __repr__(self):
        return "Username>>>> " + self.username


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    short_url = db.Column(db.String(3), unique=True, nullable=True)
    visits = db.Column(db.Integer(), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def generate_short_characters(self):
        characters = string.digits+string.ascii_letters
        picked_chars = "".join(random.choices(characters, k=3))

        link = self.query.filter_by(short_url=picked_chars).first

        if link:
            self.generate_short_characters()
        else:
            return picked_chars

    def __init__(self, **kwargs):
        super().__init__()
        self.short_url = self.generate_short_characters()

    def __repr__(self):
        return "Bookmark>>>> " + self.url
