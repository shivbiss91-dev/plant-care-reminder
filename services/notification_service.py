from datetime import date, datetime
from models import db, Notification, CareReminder, Plant

def generate_user_notifications(user_id):
    """
    Scans active reminders for a user and creates in-app notifications
    for due-today or overdue care activities if not already notified today.
    """
    today = date.today()
    active_reminders = CareReminder.query.filter_by(
        user_id=user_id,
        is_completed=False
    ).all()

    for reminder in active_reminders:
        plant = reminder.plant
        if not plant:
            continue
            
        is_overdue = reminder.due_date < today
        is_today = reminder.due_date == today
        
        if is_overdue or is_today:
            # Check if a notification for this plant and type was already created today
            existing_notif = Notification.query.filter(
                Notification.user_id == user_id,
                Notification.plant_id == plant.id,
                Notification.notification_type == reminder.reminder_type,
                Notification.created_at >= datetime(today.year, today.month, today.day)
            ).first()

            if not existing_notif:
                action_text = "watering" if reminder.reminder_type == 'watering' else "fertilizing"
                status_text = "is overdue for" if is_overdue else "needs"
                days_diff = (today - reminder.due_date).days
                
                title = f"{plant.name} {status_text} {action_text.capitalize()}!"
                if is_overdue:
                    msg = f"Your {plant.name} is {days_diff} day(s) overdue for {action_text} (due {reminder.due_date.strftime('%b %d')})."
                else:
                    msg = f"It's time to provide {action_text} for your {plant.name} today."
                    
                notif = Notification(
                    user_id=user_id,
                    plant_id=plant.id,
                    title=title,
                    message=msg,
                    notification_type=reminder.reminder_type,
                    is_read=False
                )
                db.session.add(notif)

    db.session.commit()
