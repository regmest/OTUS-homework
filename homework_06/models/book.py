from datetime import datetime
from sqlalchemy import func
from .database import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, unique=False, nullable=False)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
    )