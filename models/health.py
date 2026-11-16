from datetime import datetime
from . import db

class HealthCheckReport(db.Model):
    __tablename__ = 'health_check_reports'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id', ondelete='SET NULL'), nullable=True, index=True)
    
    plant_name = db.Column(db.String(120), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    
    symptoms = db.Column(db.Text, nullable=False)  # JSON or comma-separated symptom tags/text
    possible_issues = db.Column(db.Text, nullable=False)  # Identified potential issues
    possible_causes = db.Column(db.Text, nullable=True)   # Underlying environmental/care causes
    care_suggestions = db.Column(db.Text, nullable=True)  # Actionable remedy steps
    
    analysis_source = db.Column(db.String(50), default='rule_engine')  # 'rule_engine' or 'ai_service'
    created_at = db.Column(db.DateTime, default=datetime.now, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plant_id': self.plant_id,
            'plant_name': self.plant_name,
            'image_path': self.image_path,
            'symptoms': self.symptoms,
            'possible_issues': self.possible_issues,
            'possible_causes': self.possible_causes,
            'care_suggestions': self.care_suggestions,
            'analysis_source': self.analysis_source,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }

    def __repr__(self):
        return f'<HealthCheckReport {self.plant_name} ({self.created_at.date()})>'
