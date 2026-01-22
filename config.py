import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'database', 'itam.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload folders
    UPLOAD_FOLDER = os.path.join(basedir, 'documents', 'uploads')
    ASSIGNMENTS_FOLDER = os.path.join(basedir, 'documents', 'assignments')
    RETURNS_FOLDER = os.path.join(basedir, 'documents', 'returns')
    EXCEL_TEMPLATES_FOLDER = os.path.join(basedir, 'excel_templates')

    # Business rules - configurable per client
    DEFAULT_REPLACEMENT_YEARS = 5
    DEFAULT_ALERT_ESCALATION_DAYS = 7
    DEFAULT_MAX_MACHINES_PER_USER = 1