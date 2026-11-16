from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .plant import Plant
from .library import PlantLibrary
from .reminder import CareReminder
from .history import CareHistory
from .notification import Notification
from .health import HealthCheckReport
from .watering import WateringDecision
from .growth import GrowthRecord

__all__ = [
    'db',
    'User',
    'Plant',
    'PlantLibrary',
    'CareReminder',
    'CareHistory',
    'Notification',
    'HealthCheckReport',
    'WateringDecision',
    'GrowthRecord',
]
