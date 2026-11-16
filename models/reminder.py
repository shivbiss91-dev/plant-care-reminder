from datetime import date, datetime
from . import db

class CareReminder(db.Model):
    __tablename__ = 'care_reminders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id', ondelete='CASCADE'), nullable=False, index=True)
    
    reminder_type = db.Column(db.String(30), nullable=False)  # 'watering', 'fertilizer', 'repotting', 'pruning'
    due_date = db.Column(db.Date, nullable=False, index=True)
    frequency_days = db.Column(db.Integer, nullable=False, default=7)
    
    is_completed = db.Column(db.Boolean, default=False, index=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    @property
    def is_overdue(self):
        return not self.is_completed and self.due_date < date.today()

    @property
    def is_due_today(self):
        return not self.is_completed and self.due_date == date.today()

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plant_id': self.plant_id,
            'plant_name': self.plant.name if self.plant else 'Unknown Plant',
            'reminder_type': self.reminder_type,
            'due_date': self.due_date.isoformat(),
            'frequency_days': self.frequency_days,
            'is_completed': self.is_completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'is_overdue': self.is_overdue,
            'is_due_today': self.is_due_today,
            'notes': self.notes
        }

    def __repr__(self):
        return f'<CareReminder {self.reminder_type} for Plant {self.plant_id} due {self.due_date}>'
