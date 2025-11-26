from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Turnaround(db.Model):
    __tablename__ = 'turnaround'
    
    turnaround_id = db.Column(db.Integer, primary_key=True)
    turnaround_name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Turnaround('{self.turnaround_name}', '{self.year}')"