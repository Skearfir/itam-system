from app import db
from datetime import datetime


class Asset(db.Model):
    __tablename__ = 'assets'

    service_tag = db.Column(db.String(100), primary_key=True)
    brand = db.Column(db.String(100), nullable=False, index=True)
    model = db.Column(db.String(200), nullable=False)

    asset_tag_internal = db.Column(db.String(100), unique=True, index=True)
    asset_tag_us = db.Column(db.String(100))

    warranty_expiry = db.Column(db.Date)

    current_status = db.Column(db.String(50), nullable=False, index=True)
    # Stock, Reserved, Permanent, Temporary, Faulty, Re-dispatch Needed, Scrap, etc.

    faulty_sub_status = db.Column(db.Text)
    faulty_since_date = db.Column(db.Date)
    last_faulty_update = db.Column(db.Date)

    in_house = db.Column(db.Boolean, default=True, nullable=False)
    storage_location = db.Column(db.String(200))
    box_included = db.Column(db.Boolean)

    intune_compliance = db.Column(db.String(50))
    # Compliant, Non-Compliant, Not Enrolled, Unknown
    intune_last_checked = db.Column(db.Date)
    intune_checked_by = db.Column(db.String(100))

    currently_in_repair = db.Column(db.Boolean, default=False)

    custom_fields = db.Column(db.JSON)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    assignments = db.relationship('Assignment', backref='asset', lazy='dynamic')
    history = db.relationship('HistoryEvent', backref='asset', lazy='dynamic')

    def __repr__(self):
        return f'<Asset {self.service_tag}: {self.brand} {self.model}>'

    @property
    def total_repair_count(self):
        """Count all repair events for 3-strikes rule"""
        return self.history.filter_by(event_type='Repair').count()

    @property
    def current_assignment(self):
        """Get active assignment if any"""
        return self.assignments.filter_by(unassigned_date=None).first()