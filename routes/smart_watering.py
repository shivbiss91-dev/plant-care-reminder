from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Plant, WateringDecision
from services.watering_service import evaluate_watering_decision

smart_watering_bp = Blueprint('smart_watering', __name__, url_prefix='/smart-watering')

@smart_watering_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    user_plants = Plant.query.filter_by(user_id=current_user.id).all()
    latest_decision = None

    if request.method == 'POST':
        plant_id = request.form.get('plant_id')
        soil_condition = request.form.get('soil_condition')

        if not plant_id or not soil_condition:
            flash('Please select a plant and describe its current soil condition.', 'warning')
            return render_template('watering/index.html', plants=user_plants)

        try:
            decision = evaluate_watering_decision(
                user_id=current_user.id,
                plant_id=int(plant_id),
                soil_condition=soil_condition
            )
            latest_decision = decision
            flash(f'Smart recommendation calculated: {decision.recommendation}', 'success')
        except Exception as e:
            flash(str(e), 'danger')

    recent_decisions = WateringDecision.query.filter_by(
        user_id=current_user.id
    ).order_by(WateringDecision.created_at.desc()).limit(5).all()

    return render_template(
        'watering/index.html',
        plants=user_plants,
        latest_decision=latest_decision,
        recent_decisions=recent_decisions
    )

@smart_watering_bp.route('/history')
@login_required
def history():
    decisions = WateringDecision.query.filter_by(
        user_id=current_user.id
    ).order_by(WateringDecision.created_at.desc()).all()
    return render_template('watering/history.html', decisions=decisions)
