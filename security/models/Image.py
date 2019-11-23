from datetime import datetime

from security import db


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(20), nullable=False)
    encoding = db.Column(db.BLOB, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
