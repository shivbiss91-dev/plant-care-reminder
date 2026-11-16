from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Plant, HealthCheckReport
from services.upload_service import save_uploaded_image
from services.health_analysis_service import analyze_plant_health

health_bp = Blueprint('health', __name__, url_prefix='/health-check')

@health_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user_plants = Plant.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        plant_id_val = request.form.get('plant_id')
        manual_name = request.form.get('manual_plant_name', '').strip()
        symptoms = request.form.get('symptoms', '').strip()

        plant_id = None
        plant_name = manual_name

        if plant_id_val and plant_id_val != 'other':
            selected_plant = Plant.query.filter_by(id=int(plant_id_val), user_id=current_user.id).first()
            if selected_plant:
                plant_id = selected_plant.id
                plant_name = selected_plant.name

        if not plant_name:
            plant_name = "Unspecified Plant"

        if not symptoms:
            flash('Please describe or select the visible symptoms on your plant.', 'warning')
            return render_template('health/index.html', plants=user_plants)

        # Upload image if provided
        image_path = None
        if 'image' in request.files and request.files['image'].filename != '':
            try:
                image_path = save_uploaded_image(request.files['image'], subfolder='health_reports')
            except ValueError as e:
                flash(str(e), 'danger')
                return render_template('health/index.html', plants=user_plants)

        # Run transparent symptom analysis
        report = analyze_plant_health(
            user_id=current_user.id,
            plant_id=plant_id,
            plant_name=plant_name,
            symptoms_text=symptoms,
            image_path=image_path
        )

        flash('Health diagnosis generated successfully!', 'success')
        return redirect(url_for('health.report_detail', report_id=report.id))

    return render_template('health/index.html', plants=user_plants)

@health_bp.route('/report/<int:report_id>')
@login_required
def report_detail(report_id):
    report = HealthCheckReport.query.filter_by(id=report_id, user_id=current_user.id).first_or_404()
    return render_template('health/report.html', report=report)

@health_bp.route('/history')
@login_required
def history():
    reports = HealthCheckReport.query.filter_by(
        user_id=current_user.id
    ).order_by(HealthCheckReport.created_at.desc()).all()
    return render_template('health/history.html', reports=reports)
