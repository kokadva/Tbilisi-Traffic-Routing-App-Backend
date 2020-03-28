from datetime import datetime

from resources import db


class BusArrival(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bus_stop_id = db.Column(db.String(30), nullable=False)
    bus_num = db.Column(db.String(30), nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

