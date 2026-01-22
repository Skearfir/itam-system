from app import db
from datetime import datetime


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    max_machines_allowed = db.Column(db.Integer, default=1, nullable=False)
    description = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    users = db.relationship('User', backref='department_ref', lazy='dynamic')

    def __repr__(self):
        return f'<Department {self.name}>'