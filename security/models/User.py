from datetime import datetime

from security import db
from security.models.Image import Image


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    images = db.relationship(Image, backref='user', lazy=True)
    license_plate = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


def query(name=None, license_plate=None):
    if name:
        return User.query.filter_by(name=name).first()
    if license_plate:
        return User.query.filter_by(license_plate=license_plate).first()
