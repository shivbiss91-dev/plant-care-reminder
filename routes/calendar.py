from datetime import date, datetime, timedelta
import calendar
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from models import CareReminder, CareHistory

calendar_bp = Blueprint('calendar', __name__, url_prefix='/calendar')

@calendar_bp.route('/')
@login_required
def index():
    today = date.today()
    year = int(request.args.get('year', today.year))
    month = int(request.args.get('month', today.month))

    # Basic month navigation
    cal = calendar.Calendar(firstweekday=6)  # Sunday start
    month_days = cal.monthdatescalendar(year, month)
    
    # Previous and next month calculations
    first_day_of_month = date(year, month, 1)
    prev_month_date = (first_day_of_month - timedelta(days=1)).replace(day=1)
    next_month_date = (first_day_of_month + timedelta(days=32)).replace(day=1)

    # Fetch reminders for the displayed range
    start_date = month_days[0][0]
    end_date = month_days[-1][-1]

    reminders = CareReminder.query.filter(
        CareReminder.user_id == current_user.id,
        CareReminder.due_date >= start_date,
        CareReminder.due_date <= end_date
    ).all()

    # Group reminders by date string (YYYY-MM-DD)
    events_by_date = {}
    for r in reminders:
        d_str = r.due_date.isoformat()
        if d_str not in events_by_date:
            events_by_date[d_str] = []
        events_by_date[d_str].append(r)

    month_name = calendar.month_name[month]

    return render_template(
        'calendar/index.html',
        month_days=month_days,
        year=year,
        month=month,
        month_name=month_name,
        prev_year=prev_month_date.year,
        prev_month=prev_month_date.month,
        next_year=next_month_date.year,
        next_month=next_month_date.month,
        events_by_date=events_by_date,
        today=today
    )

@calendar_bp.route('/api/events')
@login_required
def api_events():
    """Returns JSON events for FullCalendar or JS calendar libraries."""
    reminders = CareReminder.query.filter_by(user_id=current_user.id).all()
    events = []
    for r in reminders:
        color = '#10B981' if r.reminder_type == 'watering' else '#8B5CF6'
        if r.is_completed:
            color = '#9CA3AF'
        events.append({
            'id': r.id,
            'title': f"{r.plant.name} - {r.reminder_type.capitalize()}",
            'start': r.due_date.isoformat(),
            'color': color,
            'completed': r.is_completed,
            'type': r.reminder_type
        })
    return jsonify(events)
