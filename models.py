from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Meme(db.Model):
    __tablename__ = 'memes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    permalink = db.Column(db.String, nullable=False)
