from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User
from services.upload_service import save_uploaded_image

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_profile':
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip().lower()
            email_notifs = bool(request.form.get('email_notifications'))
            browser_notifs = bool(request.form.get('browser_notifications'))

            if not username or not email:
                flash('Username and email cannot be empty.', 'danger')
                return render_template('profile/index.html')

            # Check uniqueness
            existing_user = User.query.filter(User.username == username, User.id != current_user.id).first()
            if existing_user:
                flash('Username is already taken.', 'danger')
                return render_template('profile/index.html')

            existing_email = User.query.filter(User.email == email, User.id != current_user.id).first()
            if existing_email:
                flash('Email is already registered by another account.', 'danger')
                return render_template('profile/index.html')

            current_user.username = username
            current_user.email = email
            current_user.email_notifications = email_notifs
            current_user.browser_notifications = browser_notifs

            # Handle profile image
            if 'profile_image' in request.files and request.files['profile_image'].filename != '':
                try:
                    img_path = save_uploaded_image(request.files['profile_image'], subfolder='profiles')
                    if img_path:
                        current_user.profile_image = img_path
                except ValueError as e:
                    flash(str(e), 'danger')
                    return render_template('profile/index.html')

            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile.index'))

        elif action == 'change_password':
            current_password = request.form.get('current_password', '')
            new_password = request.form.get('new_password', '')
            confirm_new_password = request.form.get('confirm_new_password', '')

            if not current_user.check_password(current_password):
                flash('Incorrect current password.', 'danger')
                return render_template('profile/index.html')

            if len(new_password) < 6:
                flash('New password must be at least 6 characters long.', 'danger')
                return render_template('profile/index.html')

            if new_password != confirm_new_password:
                flash('New passwords do not match.', 'danger')
                return render_template('profile/index.html')

            current_user.set_password(new_password)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('profile.index'))

    return render_template('profile/index.html')
