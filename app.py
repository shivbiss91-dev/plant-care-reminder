import os
from flask import Flask, send_from_directory
from flask_login import LoginManager, current_user
from config import Config
from models import db, User, Notification
from seed_data import seed_plant_library

# Import blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.plants import plants_bp
from routes.library import library_bp
from routes.reminders import reminders_bp
from routes.calendar import calendar_bp
from routes.notifications import notifications_bp
from routes.history import history_bp
from routes.profile import profile_bp
from routes.health_checker import health_bp
from routes.smart_watering import smart_watering_bp
from routes.growth_tracker import growth_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Route to securely serve uploaded images
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Context processor for global template variables
    @app.context_processor
    def inject_global_data():
        unread_count = 0
        if current_user.is_authenticated:
            unread_count = Notification.query.filter_by(
                user_id=current_user.id,
                is_read=False
            ).count()
        return {
            'unread_notifications_count': unread_count,
            'app_name': 'PlantCare'
        }

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(plants_bp)
    app.register_blueprint(library_bp)
    app.register_blueprint(reminders_bp)
    app.register_blueprint(calendar_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(smart_watering_bp)
    app.register_blueprint(growth_bp)

    # Database initialization & automated seeding
    with app.app_context():
        db.create_all()
        seed_plant_library()

    return app

app = create_app()

if __name__ == '__main__':
    # Run development server
    app.run(debug=True, host='127.0.0.1', port=5000)
