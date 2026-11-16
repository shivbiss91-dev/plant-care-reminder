from datetime import datetime
from . import db

class WateringDecision(db.Model):
    __tablename__ = 'watering_decisions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id', ondelete='CASCADE'), nullable=False, index=True)
    
    soil_condition = db.Column(db.String(50), nullable=False)  # 'Dry', 'Slightly Moist', 'Wet'
    recommendation = db.Column(db.String(50), nullable=False)  # 'Water Now', 'Wait and Check Later', 'Avoid Watering Now'
    explanation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plant_id': self.plant_id,
            'plant_name': self.plant.name if self.plant else 'Unknown Plant',
            'soil_condition': self.soil_condition,
            'recommendation': self.recommendation,
            'explanation': self.explanation,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }

    def __repr__(self):
        return f'<WateringDecision Plant {self.plant_id}: {self.recommendation}>'
