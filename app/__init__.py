from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Create upload folders
    with app.app_context():
        from app.utils.helpers import create_upload_folders
        create_upload_folders()

    # Register blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.customer import bp as customer_bp
    from app.routes.admin import bp as admin_bp
    from app.routes.orders import bp as orders_bp
    from app.routes.main import bp as main_bp
    from app.routes.delivery import bp as delivery_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp, url_prefix='/customer')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(orders_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(delivery_bp)

    return app

from app import models
