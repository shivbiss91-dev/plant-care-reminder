from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)
    
    # Notification preferences
    email_notifications = db.Column(db.Boolean, default=True)
    browser_notifications = db.Column(db.Boolean, default=True)
    
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships with cascading deletion for complete privacy and isolation
    plants = db.relationship('Plant', backref='owner', lazy='dynamic', cascade='all, delete-orphan')
    reminders = db.relationship('CareReminder', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    care_histories = db.relationship('CareHistory', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    health_reports = db.relationship('HealthCheckReport', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    watering_decisions = db.relationship('WateringDecision', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    growth_records = db.relationship('GrowthRecord', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'profile_image': self.profile_image,
            'email_notifications': self.email_notifications,
            'browser_notifications': self.browser_notifications,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

    def __repr__(self):
        return f'<User {self.username}>'
