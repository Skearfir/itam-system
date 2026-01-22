from app import db
from datetime import datetime


class HistoryEvent(db.Model):
    __tablename__ = 'history_events'

    id = db.Column(db.Integer, primary_key=True)

    service_tag = db.Column(db.String(100), db.ForeignKey('assets.service_tag'), nullable=False, index=True)
    employee_id = db.Column(db.String(50), db.ForeignKey('users.employee_id'), index=True)
    # Nullable - not all events relate to users

    event_type = db.Column(db.String(50), nullable=False, index=True)
    # Assignment, Theft, Repair, Scrap, Status Change, Location Change, AD Update, etc.

    event_date = db.Column(db.Date, nullable=False, index=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    technician = db.Column(db.String(100), nullable=False)

    # Event-specific fields
    vendor = db.Column(db.String(100))  # For repairs
    ticket_number = db.Column(db.String(100))  # DPS number, etc.
    issue_description = db.Column(db.Text)
    resolution_date = db.Column(db.Date)
    resolution_notes = db.Column(db.Text)

    scrap_method = db.Column(db.String(50))  # E-Waste, Sold, Donated, Stolen
    vendor_name = db.Column(db.String(200))  # Ware-Cycle Ltd, etc.

    from_status = db.Column(db.String(50))
    to_status = db.Column(db.String(50))

    from_location = db.Column(db.String(200))
    to_location = db.Column(db.String(200))

    notes = db.Column(db.Text)

    batch_id = db.Column(db.String(100), index=True)  # For bulk operations

    def __repr__(self):
        return f'<HistoryEvent {self.id}: {self.event_type} on {self.service_tag}>'