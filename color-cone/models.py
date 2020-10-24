from app import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(JSON)

    def __init__(self, image):
        self.image = image

    def __repr__(self):
        return '<id {}>'.format(self.id)
