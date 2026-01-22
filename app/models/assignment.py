from app import db
from datetime import datetime, timedelta
from config import Config


class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer, primary_key=True)

    service_tag = db.Column(db.String(100), db.ForeignKey('assets.service_tag'), nullable=False)
    employee_id = db.Column(db.String(50), db.ForeignKey('users.employee_id'))
    # Nullable for reserved machines

    assignment_type = db.Column(db.String(20), nullable=False)
    # Permanent, Temporary

    assigned_date = db.Column(db.Date, nullable=False, index=True)
    unassigned_date = db.Column(db.Date, index=True)
    # Null = currently active

    hostname = db.Column(db.String(100), unique=True)
    hostname_suggested = db.Column(db.String(100))
    hostname_manual_override = db.Column(db.Boolean, default=False)

    ad_description = db.Column(db.String(500))
    ad_description_manual_override = db.Column(db.Boolean, default=False)

    # For reservations before Employee ID exists
    reserved_for_email = db.Column(db.String(200))
    reserved_hire_date = db.Column(db.Date)

    # Multi-machine justification
    multiple_assignment_justification = db.Column(db.Text)
    multiple_assignment_approved_by = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String(100))  # Technician who created assignment

    def __repr__(self):
        return f'<Assignment {self.id}: {self.service_tag} → {self.employee_id or self.reserved_for_email}>'

    @property
    def is_original_machine(self):
        """Check if this is user's first machine"""
        if not self.employee_id:
            return False
        user = self.user
        return self.assigned_date == user.date_of_hire

    @property
    def replacement_due_date(self):
        """Calculate when replacement is due (5 years from assignment)"""
        years = Config.DEFAULT_REPLACEMENT_YEARS
        return self.assigned_date + timedelta(days=years * 365)

    def generate_ad_description(self):
        """Auto-generate AD description based on assignment type"""
        if self.ad_description_manual_override:
            return self.ad_description

        date_str = self.assigned_date.strftime('%Y%m%d')

        if self.assignment_type == 'Permanent' and self.employee_id:
            email = self.user.email
            return f"{email} #{date_str}"
        elif self.assignment_type == 'Temporary':
            if self.employee_id:
                email = self.user.email
                return f"Temporary Assignment - {email} #{date_str}"
            else:
                return f"Temporary Assignment #{date_str}"
        return ""