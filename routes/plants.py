from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from models import db, Plant, PlantLibrary, CareReminder, CareHistory, GrowthRecord
from services.upload_service import save_uploaded_image
from services.reminder_service import sync_plant_reminders, mark_care_activity_completed

plants_bp = Blueprint('plants', __name__, url_prefix='/plants')

@plants_bp.route('/')
@login_required
def index():
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()

    query = Plant.query.filter_by(user_id=current_user.id)

    if search_query:
        query = query.filter(
            (Plant.name.ilike(f'%{search_query}%')) |
            (Plant.species.ilike(f'%{search_query}%'))
        )

    if category_filter and category_filter != 'All':
        query = query.filter_by(category=category_filter)

    plants = query.order_by(Plant.created_at.desc()).all()
    
    # Categories for filter dropdown
    categories = ['All', 'Indoor', 'Outdoor', 'Succulent', 'Flowering', 'Herb', 'Foliage']

    return render_template(
        'plants/index.html',
        plants=plants,
        search_query=search_query,
        selected_category=category_filter or 'All',
        categories=categories
    )

@plants_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    library_id = request.args.get('library_id')
    prefill = None
    if library_id:
        prefill = PlantLibrary.query.get(library_id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', 'Indoor')
        species = request.form.get('species', '').strip()
        watering_freq = int(request.form.get('watering_frequency_days') or 7)
        fertilizer_freq = int(request.form.get('fertilizer_frequency_days') or 30)
        
        last_watered_str = request.form.get('last_watered_date')
        last_fertilized_str = request.form.get('last_fertilized_date')
        date_added_str = request.form.get('date_added')
        notes = request.form.get('notes', '').strip()

        if not name:
            flash('Plant name is required.', 'danger')
            return render_template('plants/add.html', prefill=prefill)

        last_watered = datetime.strptime(last_watered_str, '%Y-%m-%d').date() if last_watered_str else None
        last_fertilized = datetime.strptime(last_fertilized_str, '%Y-%m-%d').date() if last_fertilized_str else None
        date_added = datetime.strptime(date_added_str, '%Y-%m-%d').date() if date_added_str else date.today()

        # Handle image upload
        image_path = None
        if 'image' in request.files and request.files['image'].filename != '':
            try:
                image_path = save_uploaded_image(request.files['image'], subfolder='plants')
            except ValueError as e:
                flash(str(e), 'danger')
                return render_template('plants/add.html', prefill=prefill)

        new_plant = Plant(
            user_id=current_user.id,
            name=name,
            category=category,
            species=species,
            watering_frequency_days=watering_freq,
            fertilizer_frequency_days=fertilizer_freq,
            last_watered_date=last_watered,
            last_fertilized_date=last_fertilized,
            date_added=date_added,
            image_path=image_path,
            notes=notes
        )
        db.session.add(new_plant)
        db.session.commit()

        # Automatically create initial schedule reminders
        sync_plant_reminders(new_plant)

        flash(f'Plant "{new_plant.name}" added successfully to your garden!', 'success')
        return redirect(url_for('plants.detail', plant_id=new_plant.id))

    return render_template('plants/add.html', prefill=prefill)

@plants_bp.route('/<int:plant_id>')
@login_required
def detail(plant_id):
    plant = Plant.query.filter_by(id=plant_id, user_id=current_user.id).first_or_404()
    
    # Care history for this plant
    history = CareHistory.query.filter_by(
        user_id=current_user.id,
        plant_id=plant.id
    ).order_by(CareHistory.activity_date.desc()).limit(10).all()

    # Growth records for this plant
    growth_records = GrowthRecord.query.filter_by(
        user_id=current_user.id,
        plant_id=plant.id
    ).order_by(GrowthRecord.observation_date.desc()).limit(5).all()

    return render_template(
        'plants/detail.html',
        plant=plant,
        history=history,
        growth_records=growth_records
    )

@plants_bp.route('/<int:plant_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(plant_id):
    plant = Plant.query.filter_by(id=plant_id, user_id=current_user.id).first_or_404()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            flash('Plant name is required.', 'danger')
            return render_template('plants/edit.html', plant=plant)

        plant.name = name
        plant.category = request.form.get('category', plant.category)
        plant.species = request.form.get('species', '').strip()
        plant.watering_frequency_days = int(request.form.get('watering_frequency_days') or 7)
        plant.fertilizer_frequency_days = int(request.form.get('fertilizer_frequency_days') or 30)

        last_watered_str = request.form.get('last_watered_date')
        last_fertilized_str = request.form.get('last_fertilized_date')
        if last_watered_str:
            plant.last_watered_date = datetime.strptime(last_watered_str, '%Y-%m-%d').date()
        if last_fertilized_str:
            plant.last_fertilized_date = datetime.strptime(last_fertilized_str, '%Y-%m-%d').date()

        plant.notes = request.form.get('notes', '').strip()

        # Handle image replacement
        if 'image' in request.files and request.files['image'].filename != '':
            try:
                new_image = save_uploaded_image(request.files['image'], subfolder='plants')
                if new_image:
                    plant.image_path = new_image
            except ValueError as e:
                flash(str(e), 'danger')
                return render_template('plants/edit.html', plant=plant)

        db.session.commit()
        sync_plant_reminders(plant)

        flash(f'Plant "{plant.name}" updated successfully.', 'success')
        return redirect(url_for('plants.detail', plant_id=plant.id))

    return render_template('plants/edit.html', plant=plant)

@plants_bp.route('/<int:plant_id>/delete', methods=['POST'])
@login_required
def delete(plant_id):
    plant = Plant.query.filter_by(id=plant_id, user_id=current_user.id).first_or_404()
    plant_name = plant.name
    db.session.delete(plant)
    db.session.commit()
    flash(f'Plant "{plant_name}" was deleted successfully.', 'info')
    return redirect(url_for('plants.index'))

@plants_bp.route('/<int:plant_id>/water', methods=['POST'])
@login_required
def quick_water(plant_id):
    mark_care_activity_completed(current_user.id, plant_id, 'watering')
    flash('Marked as watered today! Next watering schedule updated.', 'success')
    return redirect(request.referrer or url_for('plants.detail', plant_id=plant_id))

@plants_bp.route('/<int:plant_id>/fertilize', methods=['POST'])
@login_required
def quick_fertilize(plant_id):
    mark_care_activity_completed(current_user.id, plant_id, 'fertilizer')
    flash('Marked as fertilized today! Next fertilizer schedule updated.', 'success')
    return redirect(request.referrer or url_for('plants.detail', plant_id=plant_id))
