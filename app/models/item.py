from core.main import db
from core.models import Model


class Item(Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(30), nullable=False)
    request_date = db.Column(db.Date, nullable=False)
    remarks =db.Column(db.String(5000), nullable=True)
    created_at = db.Column(db.DateTime(timezone=False), nullable=False)
