from ..extensions import db
from sqlalchemy.sql import text
from datetime import datetime

class Turnaround(db.Model):
    __tablename__ = 'turnaround'

    # Primary Key
    turnaround_id = db.Column(db.Integer, primary_key=True)

    # Attributes
    turnaround_name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    # Timestamp
    created_at = db.Column(
        db.DateTime,
        server_default=text('NOW()'),
        nullable=False
    )

    # ---------------------------
    # 🔗 Relationships
    # ---------------------------
    inspections = db.relationship(
        'Inspection',
        backref='turnaround'
    )

    # ---------------------------
    # String Representation
    # ---------------------------
    def __repr__(self):
        return f"<Turnaround {self.turnaround_id} - {self.turnaround_name} ({self.year})>"

    # ---------------------------
    # Convert to Dictionary
    # ---------------------------
    def to_dict(self):
        return {
            'turnaround_id': self.turnaround_id,
            'turnaround_name': self.turnaround_name,
            'year': self.year,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at
        }
