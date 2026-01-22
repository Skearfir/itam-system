from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['ASSIGNMENTS_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RETURNS_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, '..', 'database'), exist_ok=True)

    # Import models so Flask-Migrate can detect them
    from app.models import asset, user, assignment, history, department

    # Register blueprints
    from app.routes import main
    from app.routes import views  # Import views AFTER main blueprint exists
    app.register_blueprint(main)

    return app