from datetime import datetime
from . import db

class PlantLibrary(db.Model):
    __tablename__ = 'plant_library'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    scientific_name = db.Column(db.String(150), nullable=True)
    category = db.Column(db.String(80), nullable=True, default='Indoor')
    description = db.Column(db.Text, nullable=True)
    
    watering_requirements = db.Column(db.Text, nullable=True)
    fertilizer_requirements = db.Column(db.Text, nullable=True)
    sunlight_requirements = db.Column(db.Text, nullable=True)
    soil_requirements = db.Column(db.Text, nullable=True)
    care_instructions = db.Column(db.Text, nullable=True)
    
    default_watering_frequency_days = db.Column(db.Integer, default=7)
    default_fertilizer_frequency_days = db.Column(db.Integer, default=30)
    sample_image = db.Column(db.String(255), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'scientific_name': self.scientific_name,
            'category': self.category,
            'description': self.description,
            'watering_requirements': self.watering_requirements,
            'fertilizer_requirements': self.fertilizer_requirements,
            'sunlight_requirements': self.sunlight_requirements,
            'soil_requirements': self.soil_requirements,
            'care_instructions': self.care_instructions,
            'default_watering_frequency_days': self.default_watering_frequency_days,
            'default_fertilizer_frequency_days': self.default_fertilizer_frequency_days,
            'sample_image': self.sample_image
        }

    def __repr__(self):
        return f'<PlantLibrary {self.name}>'
