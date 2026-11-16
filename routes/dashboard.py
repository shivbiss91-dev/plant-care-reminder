from datetime import date
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import Plant, CareReminder, Notification, GrowthRecord
from services.notification_service import generate_user_notifications

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))

@dashboard_bp.route('/dashboard')
@login_required
def index():
    # Sync in-app notifications for today
    generate_user_notifications(current_user.id)
    
    today = date.today()
    user_plants = Plant.query.filter_by(user_id=current_user.id).all()
    total_plants = len(user_plants)
    
    # Plants needing water today or overdue
    plants_need_water = [p for p in user_plants if p.needs_watering]
    
    # Upcoming fertilizer reminders (active within next 7 days)
    upcoming_fertilizer = CareReminder.query.filter(
        CareReminder.user_id == current_user.id,
        CareReminder.reminder_type == 'fertilizer',
        CareReminder.is_completed == False,
        CareReminder.due_date <= today
    ).all()
    
    # Today's active care reminders
    todays_activities = CareReminder.query.filter(
        CareReminder.user_id == current_user.id,
        CareReminder.due_date == today,
        CareReminder.is_completed == False
    ).all()

    # Recent notifications (last 5)
    recent_notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).limit(5).all()

    # Recent plant growth updates (last 4)
    recent_growth = GrowthRecord.query.filter_by(
        user_id=current_user.id
    ).order_by(GrowthRecord.observation_date.desc(), GrowthRecord.created_at.desc()).limit(4).all()

    return render_template(
        'dashboard.html',
        total_plants=total_plants,
        plants_need_water=plants_need_water,
        upcoming_fertilizer=upcoming_fertilizer,
        todays_activities=todays_activities,
        recent_notifications=recent_notifications,
        recent_growth=recent_growth,
        today=today
    )
