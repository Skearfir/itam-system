from flask import render_template
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