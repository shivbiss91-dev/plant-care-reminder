import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret-key-plantcare-change-in-production')
    
    # Handle serverless read-only filesystem environments (e.g. Vercel)
    is_serverless = os.environ.get('VERCEL') == '1'
    
    if is_serverless:
        INSTANCE_DIR = '/tmp/instance'
        UPLOAD_FOLDER = '/tmp/uploads'
    else:
        INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
        UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
        
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    
    db_file = os.path.join(INSTANCE_DIR, 'plantcare.db').replace('\\', '/')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_file}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File Upload Configuration
    UPLOAD_PLANTS = os.path.join(UPLOAD_FOLDER, 'plants')
    UPLOAD_HEALTH = os.path.join(UPLOAD_FOLDER, 'health_reports')
    UPLOAD_GROWTH = os.path.join(UPLOAD_FOLDER, 'growth')
    UPLOAD_PROFILES = os.path.join(UPLOAD_FOLDER, 'profiles')
    
    for folder in [UPLOAD_PLANTS, UPLOAD_HEALTH, UPLOAD_GROWTH, UPLOAD_PROFILES]:
        os.makedirs(folder, exist_ok=True)
        
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
