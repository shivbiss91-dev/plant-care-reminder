from datetime import date, datetime
from . import db

class CareHistory(db.Model):
    __tablename__ = 'care_histories'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id', ondelete='SET NULL'), nullable=True, index=True)
    
    plant_name = db.Column(db.String(120), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)  # watering, fertilizing, pruning, repotting, misting
    activity_date = db.Column(db.Date, nullable=False, default=date.today)
    activity_description = db.Column(db.Text, nullable=True)
    completion_status = db.Column(db.String(30), default='completed')  # completed, skipped
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plant_id': self.plant_id,
            'plant_name': self.plant_name,
            'activity_type': self.activity_type,
            'activity_date': self.activity_date.isoformat(),
            'activity_description': self.activity_description,
            'completion_status': self.completion_status,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }

    def __repr__(self):
        return f'<CareHistory {self.activity_type} for {self.plant_name} on {self.activity_date}>'
