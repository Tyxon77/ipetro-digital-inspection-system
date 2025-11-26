from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Remove the relative import, we'll get db from app.py later
db = SQLAlchemy()

class Equipment(db.Model):
    __tablename__ = 'equipment'
    
    equipment_id = db.Column(db.Integer, primary_key=True)
    equipment_tag = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(100))
    type = db.Column(db.String(50))
    service = db.Column(db.String(50))
    pml_number = db.Column(db.String(50))
    dosh_number = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Equipment('{self.equipment_tag}', '{self.description}')"