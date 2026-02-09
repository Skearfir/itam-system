from flask import render_template, jsonify
from app.routes import main
from app.models import Asset, User, Assignment, HistoryEvent, Department
from app import db

@main.route('/')
def index():
    """Dashboard/Home page"""
    total_assets = Asset.query.count()
    stock_count = Asset.query.filter_by(current_status='Stock').count()
    assigned_count = Asset.query.filter(Asset.current_status.in_(['Permanent', 'Temporary'])).count()
    faulty_count = Asset.query.filter_by(current_status='Faulty').count()
    reserved_count = Asset.query.filter_by(current_status='Reserved').count()
    active_users = User.query.filter_by(employment_status='Active').count()

    # Recent events (last 10)
    recent_events = HistoryEvent.query.order_by(HistoryEvent.created_timestamp.desc()).limit(10).all()

    # Faulty machines for alerts
    faulty_machines = Asset.query.filter_by(current_status='Faulty').all()

    return render_template('index.html',
                           total_assets=total_assets,
                           stock_count=stock_count,
                           assigned_count=assigned_count,
                           faulty_count=faulty_count,
                           reserved_count=reserved_count,
                           active_users=active_users,
                           recent_events=recent_events,
                           faulty_machines=faulty_machines)


@main.route('/assets')
def assets():
    """Asset list page"""
    assets = Asset.query.all()

    total_assets = len(assets)
    stock_count = Asset.query.filter_by(current_status='Stock').count()
    assigned_count = Asset.query.filter(Asset.current_status.in_(['Permanent', 'Temporary'])).count()
    faulty_count = Asset.query.filter_by(current_status='Faulty').count()

    return render_template('assets.html',
                           assets=assets,
                           total_assets=total_assets,
                           stock_count=stock_count,
                           assigned_count=assigned_count,
                           faulty_count=faulty_count)


@main.route('/assets/<service_tag>')
def asset_detail(service_tag):
    """Asset detail page (placeholder for now)"""
    asset = Asset.query.get_or_404(service_tag)
    return f"<h1>Asset Detail: {service_tag}</h1><p>Coming soon!</p>"


@main.route('/users')
def users():
    """Users list page"""
    users = User.query.all()
    return render_template('users.html', users=users)


@main.route('/api/asset/<service_tag>')
def api_asset_detail(service_tag):
    """API endpoint to fetch asset details"""
    asset = Asset.query.get_or_404(service_tag)

    # Get current assignment (where unassigned_date is None)
    current_assignment = Assignment.query.filter_by(
        service_tag=service_tag,
        unassigned_date=None
    ).first()

    # Get assignment history (all assignments for this asset)
    assignment_history = Assignment.query.filter_by(
        service_tag=service_tag
    ).order_by(Assignment.assigned_date.desc()).all()

    # Get asset history
    history_events = HistoryEvent.query.filter_by(
        service_tag=service_tag
    ).order_by(HistoryEvent.created_timestamp.desc()).all()

    # Helper function to get department name
    def get_department_name(user):
        if not user or not user.department_id:
            return 'Unknown'
        dept = Department.query.get(user.department_id)
        return dept.name if dept else 'Unknown'

    return jsonify({
        'asset': {
            'service_tag': asset.service_tag,
            'brand': asset.brand,
            'model': asset.model,
            'hostname': getattr(asset, 'hostname', None),
            'asset_tag_internal': asset.asset_tag_internal,
            'asset_tag_us': asset.asset_tag_us,
            'current_status': asset.current_status,
            'faulty_sub_status': asset.faulty_sub_status,
            'warranty_expiry': asset.warranty_expiry.strftime('%Y-%m-%d') if asset.warranty_expiry else None,
            'purchase_date': getattr(asset, 'purchase_date', None).strftime('%Y-%m-%d') if getattr(asset,
                                                                                                   'purchase_date',
                                                                                                   None) else None,
            'ram_gb': getattr(asset, 'ram_gb', None),
            'storage_info': getattr(asset, 'storage_info', None),
            'processor': getattr(asset, 'processor', None),
            'in_house': asset.in_house,
            'storage_location': asset.storage_location,
            'notes': getattr(asset, 'notes', None),
            'custom_fields': asset.custom_fields or {}
        },

        'current_assignment': {
            'employee_id': current_assignment.employee_id,
            'full_name': current_assignment.user.full_name if current_assignment.user else 'Reserved',
            'email': current_assignment.user.email if current_assignment.user else current_assignment.reserved_for_email,
            'department': get_department_name(current_assignment.user),
            'assigned_date': current_assignment.assigned_date.strftime('%Y-%m-%d'),
            'assignment_type': current_assignment.assignment_type,
            'hostname': current_assignment.hostname
        } if current_assignment else None,
        'assignment_history': [
            {
                'employee_id': a.employee_id or 'Reserved',
                'full_name': a.user.full_name if a.user else 'Reserved',
                'assigned_date': a.assigned_date.strftime('%Y-%m-%d'),
                'unassigned_date': a.unassigned_date.strftime('%Y-%m-%d') if a.unassigned_date else 'Current',
                'assignment_type': a.assignment_type,
                'hostname': a.hostname
            } for a in assignment_history
        ],
        'history': [
            {
                'event_date': h.event_date.strftime('%Y-%m-%d') if h.event_date else 'Unknown',
                'event_type': h.event_type,
                'technician': h.technician,
                'notes': h.notes,
                'timestamp': h.created_timestamp.strftime('%Y-%m-%d %H:%M')
            } for h in history_events
        ]
    })