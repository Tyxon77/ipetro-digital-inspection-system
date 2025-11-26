from ..extensions import db
from sqlalchemy.sql import text
from datetime import datetime

class Equipment(db.Model):
    __tablename__ = 'equipment'

    # Primary Key
    equipment_id = db.Column(db.Integer, primary_key=True)

    # Attributes
    equipment_tag = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    type = db.Column(db.String(50), nullable=True)
    service = db.Column(db.String(100), nullable=True)
    pml_number = db.Column(db.String(50), nullable=True)
    dosh_number = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Foreign Key → User
    created_by_user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.user_id'),
        nullable=False
    )

    # Timestamp
    created_at = db.Column(
        db.DateTime,
        server_default=text('NOW()'),
        nullable=False
    )

    # ---------------------------
    # 🔗 Relationships
    # ---------------------------
    created_by = db.relationship(
        'User',
        backref='created_equipments'
    )

    inspections = db.relationship(
        'Inspection',
        backref='equipment'
    )

    # ---------------------------
    # String Representation
    # ---------------------------
    def __repr__(self):
        return f"<Equipment {self.equipment_id} - {self.equipment_tag}>"

    # ---------------------------
    # Convert to Dictionary
    # ---------------------------
    def to_dict(self):
        return {
            'equipment_id': self.equipment_id,
            'equipment_tag': self.equipment_tag,
            'description': self.description,
            'location': self.location,
            'type': self.type,
            'service': self.service,
            'pml_number': self.pml_number,
            'dosh_number': self.dosh_number,
            'is_active': self.is_active,
            'created_by_user_id': self.created_by_user_id,
            'created_at': self.created_at
        }
