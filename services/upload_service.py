import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
from flask import current_app

def allowed_file(filename):
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'webp', 'gif'})

def save_uploaded_image(file_storage, subfolder='plants'):
    """
    Validates and securely saves an uploaded image file into the specified subfolder.
    Returns the relative path for database storage (e.g. 'uploads/plants/xyz.jpg') or None.
    """
    if not file_storage or file_storage.filename == '':
        return None

    if not allowed_file(file_storage.filename):
        raise ValueError("Invalid file type. Allowed formats: PNG, JPG, JPEG, WEBP, GIF.")

    # Validate image authenticity with Pillow to prevent malicious polyglot/executable files
    try:
        image = Image.open(file_storage.stream)
        image.verify()
        file_storage.stream.seek(0)
    except Exception:
        raise ValueError("Uploaded file is corrupted or not a valid image.")

    # Generate a unique, collision-resistant filename
    original_filename = secure_filename(file_storage.filename)
    extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
    unique_filename = f"{uuid.uuid4().hex}_{int(os.path.getmtime(file_storage.stream.fileno()) if hasattr(file_storage.stream, 'fileno') else 0)}.{extension}"
    
    target_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(target_dir, exist_ok=True)
    
    file_path = os.path.join(target_dir, unique_filename)
    file_storage.save(file_path)
    
    # Return path relative to project root or accessible via static route
    return f"uploads/{subfolder}/{unique_filename}"
