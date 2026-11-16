from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Plant, GrowthRecord
from services.upload_service import save_uploaded_image

growth_bp = Blueprint('growth', __name__, url_prefix='/growth-tracker')

@growth_bp.route('/')
@login_required
def index():
    plants = Plant.query.filter_by(user_id=current_user.id).all()
    # Find plants with growth records
    plant_summaries = []
    for plant in plants:
        records = GrowthRecord.query.filter_by(
            user_id=current_user.id,
            plant_id=plant.id
        ).order_by(GrowthRecord.observation_date.asc()).all()

        first_record = records[0] if records else None
        latest_record = records[-1] if records else None
        
        height_diff = None
        if first_record and latest_record and first_record.height_cm and latest_record.height_cm:
            height_diff = round(latest_record.height_cm - first_record.height_cm, 1)

        plant_summaries.append({
            'plant': plant,
            'record_count': len(records),
            'latest_record': latest_record,
            'height_diff': height_diff
        })

    return render_template('growth/index.html', plant_summaries=plant_summaries, plants=plants)

@growth_bp.route('/plant/<int:plant_id>', methods=['GET', 'POST'])
@login_required
def plant_timeline(plant_id):
    plant = Plant.query.filter_by(id=plant_id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        obs_date_str = request.form.get('observation_date')
        height_str = request.form.get('height_cm')
        condition = request.form.get('condition', 'Healthy')
        notes = request.form.get('notes', '').strip()

        obs_date = datetime.strptime(obs_date_str, '%Y-%m-%d').date() if obs_date_str else date.today()
        height_cm = float(height_str) if height_str and height_str.strip() else None

        image_path = None
        if 'image' in request.files and request.files['image'].filename != '':
            try:
                image_path = save_uploaded_image(request.files['image'], subfolder='growth')
            except ValueError as e:
                flash(str(e), 'danger')
                return redirect(url_for('growth.plant_timeline', plant_id=plant.id))

        new_record = GrowthRecord(
            user_id=current_user.id,
            plant_id=plant.id,
            observation_date=obs_date,
            height_cm=height_cm,
            condition=condition,
            image_path=image_path,
            notes=notes
        )
        db.session.add(new_record)
        db.session.commit()
        flash('Growth record added successfully!', 'success')
        return redirect(url_for('growth.plant_timeline', plant_id=plant.id))

    records = GrowthRecord.query.filter_by(
        user_id=current_user.id,
        plant_id=plant.id
    ).order_by(GrowthRecord.observation_date.desc()).all()

    # Oldest record for photo comparison
    oldest_record = GrowthRecord.query.filter(
        GrowthRecord.user_id == current_user.id,
        GrowthRecord.plant_id == plant.id,
        GrowthRecord.image_path.isnot(None)
    ).order_by(GrowthRecord.observation_date.asc()).first()

    latest_record_with_img = GrowthRecord.query.filter(
        GrowthRecord.user_id == current_user.id,
        GrowthRecord.plant_id == plant.id,
        GrowthRecord.image_path.isnot(None)
    ).order_by(GrowthRecord.observation_date.desc()).first()

    return render_template(
        'growth/timeline.html',
        plant=plant,
        records=records,
        oldest_record=oldest_record,
        latest_record_with_img=latest_record_with_img,
        today=date.today()
    )
