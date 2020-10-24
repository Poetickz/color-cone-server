from app import db

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String())

    def __init__(self, image):
        self.image = image

    def __repr__(self):
        return '<id {}>'.format(self.id)