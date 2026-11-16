from datetime import date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import CareReminder
from services.reminder_service import mark_care_activity_completed

reminders_bp = Blueprint('reminders', __name__, url_prefix='/reminders')

@reminders_bp.route('/')
@login_required
def index():
    today = date.today()
    reminder_type = request.args.get('type', 'all')  # 'all', 'watering', 'fertilizer'
    status_filter = request.args.get('status', 'active')  # 'active', 'completed', 'all'

    query = CareReminder.query.filter_by(user_id=current_user.id)

    if reminder_type in ['watering', 'fertilizer']:
        query = query.filter_by(reminder_type=reminder_type)

    if status_filter == 'active':
        query = query.filter_by(is_completed=False)
    elif status_filter == 'completed':
        query = query.filter_by(is_completed=True)

    reminders = query.order_by(CareReminder.due_date.asc()).all()

    # Categorize active reminders
    overdue_list = [r for r in reminders if not r.is_completed and r.due_date < today]
    today_list = [r for r in reminders if not r.is_completed and r.due_date == today]
    upcoming_list = [r for r in reminders if not r.is_completed and r.due_date > today]
    completed_list = [r for r in reminders if r.is_completed]

    return render_template(
        'reminders/index.html',
        overdue_list=overdue_list,
        today_list=today_list,
        upcoming_list=upcoming_list,
        completed_list=completed_list,
        all_reminders=reminders,
        current_type=reminder_type,
        current_status=status_filter,
        today=today
    )

@reminders_bp.route('/complete/<int:reminder_id>', methods=['POST'])
@login_required
def complete(reminder_id):
    reminder = CareReminder.query.filter_by(id=reminder_id, user_id=current_user.id).first_or_404()
    mark_care_activity_completed(
        user_id=current_user.id,
        plant_id=reminder.plant_id,
        activity_type=reminder.reminder_type,
        activity_date=date.today(),
        notes=request.form.get('notes')
    )
    flash(f'Marked {reminder.reminder_type} for {reminder.plant.name} as completed!', 'success')
    return redirect(request.referrer or url_for('reminders.index'))
