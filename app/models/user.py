from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    employee_id = db.Column(db.String(50), primary_key=True)
    full_name = db.Column(db.String(200), nullable=False, index=True)
    email = db.Column(db.String(200), nullable=False, unique=True, index=True)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    date_of_hire = db.Column(db.Date, nullable=False)
    employment_status = db.Column(db.String(20), default='Active', nullable=False)
    # Active, On Leave, Terminated

    manager = db.Column(db.String(200))  # Manual for now, AD sync later
    custom_fields = db.Column(db.JSON)  # Flexible storage for client-specific needs

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    assignments = db.relationship('Assignment', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.employee_id}: {self.full_name}>'

    @property
    def active_assignments_count(self):
        """Count current active assignments"""
        return self.assignments.filter_by(unassigned_date=None).count()