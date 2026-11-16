from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import CareHistory, Plant

history_bp = Blueprint('history', __name__, url_prefix='/history')

@history_bp.route('/')
@login_required
def index():
    activity_filter = request.args.get('type', 'all')
    plant_filter = request.args.get('plant_id', 'all')

    query = CareHistory.query.filter_by(user_id=current_user.id)

    if activity_filter and activity_filter != 'all':
        query = query.filter_by(activity_type=activity_filter)

    if plant_filter and plant_filter != 'all':
        query = query.filter_by(plant_id=int(plant_filter))

    records = query.order_by(CareHistory.activity_date.desc(), CareHistory.created_at.desc()).all()
    user_plants = Plant.query.filter_by(user_id=current_user.id).all()

    return render_template(
        'history/index.html',
        records=records,
        plants=user_plants,
        selected_type=activity_filter,
        selected_plant=plant_filter
    )
