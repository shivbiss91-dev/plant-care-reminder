from datetime import date, datetime
from . import db

class GrowthRecord(db.Model):
    __tablename__ = 'growth_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id', ondelete='CASCADE'), nullable=False, index=True)
    
    observation_date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    height_cm = db.Column(db.Float, nullable=True)
    condition = db.Column(db.String(50), nullable=True, default='Healthy')  # 'Healthy', 'Flourishing', 'Moderate', 'Struggling'
    image_path = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plant_id': self.plant_id,
            'plant_name': self.plant.name if self.plant else 'Unknown Plant',
            'observation_date': self.observation_date.isoformat(),
            'height_cm': self.height_cm,
            'condition': self.condition,
            'image_path': self.image_path,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }

    def __repr__(self):
        return f'<GrowthRecord Plant {self.plant_id} on {self.observation_date}>'
