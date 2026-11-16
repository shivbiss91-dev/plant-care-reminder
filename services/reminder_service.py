from datetime import date, timedelta, datetime
from models import db, CareReminder, CareHistory, Plant, Notification

def sync_plant_reminders(plant):
    """
    Ensures active watering and fertilizer reminders exist for a given plant.
    """
    today = date.today()
    
    # 1. Watering Reminder
    water_reminder = CareReminder.query.filter_by(
        plant_id=plant.id,
        user_id=plant.user_id,
        reminder_type='watering',
        is_completed=False
    ).first()
    
    expected_water_date = plant.next_watering_date
    if not water_reminder:
        water_reminder = CareReminder(
            user_id=plant.user_id,
            plant_id=plant.id,
            reminder_type='watering',
            due_date=expected_water_date,
            frequency_days=plant.watering_frequency_days or 7,
            notes=f"Scheduled watering every {plant.watering_frequency_days or 7} days."
        )
        db.session.add(water_reminder)
    else:
        water_reminder.due_date = expected_water_date
        water_reminder.frequency_days = plant.watering_frequency_days or 7

    # 2. Fertilizer Reminder
    fertilizer_reminder = CareReminder.query.filter_by(
        plant_id=plant.id,
        user_id=plant.user_id,
        reminder_type='fertilizer',
        is_completed=False
    ).first()
    
    expected_fert_date = plant.next_fertilizer_date
    if not fertilizer_reminder:
        fertilizer_reminder = CareReminder(
            user_id=plant.user_id,
            plant_id=plant.id,
            reminder_type='fertilizer',
            due_date=expected_fert_date,
            frequency_days=plant.fertilizer_frequency_days or 30,
            notes=f"Scheduled fertilizer every {plant.fertilizer_frequency_days or 30} days."
        )
        db.session.add(fertilizer_reminder)
    else:
        fertilizer_reminder.due_date = expected_fert_date
        fertilizer_reminder.frequency_days = plant.fertilizer_frequency_days or 30

    db.session.commit()

def mark_care_activity_completed(user_id, plant_id, activity_type, activity_date=None, notes=None):
    """
    Marks a care activity (watering or fertilizing) as completed:
    - Updates plant last performed date
    - Logs into CareHistory
    - Marks matching active reminder as completed
    - Spawns the next reminder cycle
    """
    plant = Plant.query.filter_by(id=plant_id, user_id=user_id).first_or_404()
    actual_date = activity_date or date.today()
    
    if activity_type == 'watering':
        plant.last_watered_date = actual_date
        desc = f"Watered {plant.name} according to care schedule."
        freq = plant.watering_frequency_days or 7
    elif activity_type == 'fertilizer':
        plant.last_fertilized_date = actual_date
        desc = f"Applied fertilizer nutrients to {plant.name}."
        freq = plant.fertilizer_frequency_days or 30
    else:
        desc = f"Completed {activity_type} for {plant.name}."
        freq = 7

    # 1. Log Care History
    history_entry = CareHistory(
        user_id=user_id,
        plant_id=plant.id,
        plant_name=plant.name,
        activity_type=activity_type,
        activity_date=actual_date,
        activity_description=desc,
        completion_status='completed',
        notes=notes
    )
    db.session.add(history_entry)

    # 2. Mark existing reminder as completed
    existing_reminder = CareReminder.query.filter_by(
        user_id=user_id,
        plant_id=plant.id,
        reminder_type=activity_type,
        is_completed=False
    ).first()

    if existing_reminder:
        existing_reminder.is_completed = True
        existing_reminder.completed_at = datetime.now()

    # 3. Create next cycle reminder
    next_due = actual_date + timedelta(days=freq)
    next_reminder = CareReminder(
        user_id=user_id,
        plant_id=plant.id,
        reminder_type=activity_type,
        due_date=next_due,
        frequency_days=freq,
        is_completed=False,
        notes=f"Next {activity_type} cycle."
    )
    db.session.add(next_reminder)

    db.session.commit()
    return history_entry
