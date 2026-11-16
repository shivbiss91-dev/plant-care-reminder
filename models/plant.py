from datetime import date, datetime, timedelta
from . import db

class Plant(db.Model):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80), nullable=True, default='Indoor')  # Indoor, Outdoor, Succulent, Flowering, Herb, Foliage
    species = db.Column(db.String(120), nullable=True)
    image_path = db.Column(db.String(255), nullable=True)
    
    # Care frequencies in days
    watering_frequency_days = db.Column(db.Integer, nullable=False, default=7)
    fertilizer_frequency_days = db.Column(db.Integer, nullable=False, default=30)
    
    # Last performed dates
    last_watered_date = db.Column(db.Date, nullable=True)
    last_fertilized_date = db.Column(db.Date, nullable=True)
    
    date_added = db.Column(db.Date, default=date.today)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    reminders = db.relationship('CareReminder', backref='plant', lazy='dynamic', cascade='all, delete-orphan')
    care_histories = db.relationship('CareHistory', backref='plant', lazy='dynamic', cascade='all, delete-orphan')
    health_reports = db.relationship('HealthCheckReport', backref='plant', lazy='dynamic')
    watering_decisions = db.relationship('WateringDecision', backref='plant', lazy='dynamic', cascade='all, delete-orphan')
    growth_records = db.relationship('GrowthRecord', backref='plant', lazy='dynamic', cascade='all, delete-orphan')

    @property
    def next_watering_date(self):
        if not self.last_watered_date:
            return self.date_added or date.today()
        return self.last_watered_date + timedelta(days=self.watering_frequency_days or 7)

    @property
    def next_fertilizer_date(self):
        if not self.last_fertilized_date:
            return self.date_added or date.today()
        return self.last_fertilized_date + timedelta(days=self.fertilizer_frequency_days or 30)

    @property
    def days_until_watering(self):
        next_date = self.next_watering_date
        return (next_date - date.today()).days

    @property
    def days_until_fertilizer(self):
        next_date = self.next_fertilizer_date
        return (next_date - date.today()).days

    @property
    def needs_watering(self):
        return self.days_until_watering <= 0

    @property
    def needs_fertilizer(self):
        return self.days_until_fertilizer <= 0

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'category': self.category,
            'species': self.species,
            'image_path': self.image_path,
            'watering_frequency_days': self.watering_frequency_days,
            'fertilizer_frequency_days': self.fertilizer_frequency_days,
            'last_watered_date': self.last_watered_date.isoformat() if self.last_watered_date else None,
            'last_fertilized_date': self.last_fertilized_date.isoformat() if self.last_fertilized_date else None,
            'next_watering_date': self.next_watering_date.isoformat() if self.next_watering_date else None,
            'next_fertilizer_date': self.next_fertilizer_date.isoformat() if self.next_fertilizer_date else None,
            'needs_watering': self.needs_watering,
            'needs_fertilizer': self.needs_fertilizer,
            'days_until_watering': self.days_until_watering,
            'days_until_fertilizer': self.days_until_fertilizer,
            'date_added': self.date_added.isoformat() if self.date_added else None,
            'notes': self.notes
        }

    def __repr__(self):
        return f'<Plant {self.name}>'
