"""
Script to create a default demonstration user and sample plants, reminders, and growth records.
"""
from datetime import date, timedelta
from app import create_app
from models import db, User, Plant, CareReminder, CareHistory, GrowthRecord, Notification
from services.reminder_service import sync_plant_reminders

app = create_app()

with app.app_context():
    # Check if demo user already exists
    demo_user = User.query.filter_by(username='demo_student').first()
    if not demo_user:
        demo_user = User(
            username='demo_student',
            email='demo@college.edu',
            email_notifications=True,
            browser_notifications=True
        )
        demo_user.set_password('plantcare123')
        db.session.add(demo_user)
        db.session.commit()
        print("Created demo user: username='demo_student', password='plantcare123'")

    # Check if demo user has plants
    if demo_user.plants.count() == 0:
        today = date.today()

        # Plant 1: Monstera (Healthy, next water in 3 days)
        p1 = Plant(
            user_id=demo_user.id,
            name="Living Room Monstera",
            category="Indoor",
            species="Monstera deliciosa",
            watering_frequency_days=7,
            fertilizer_frequency_days=30,
            last_watered_date=today - timedelta(days=4),
            last_fertilized_date=today - timedelta(days=15),
            date_added=today - timedelta(days=60),
            notes="Placed near north-facing French window. Loves regular misting."
        )

        # Plant 2: Peace Lily (Needs water today!)
        p2 = Plant(
            user_id=demo_user.id,
            name="Bedroom Peace Lily",
            category="Flowering",
            species="Spathiphyllum wallisii",
            watering_frequency_days=5,
            fertilizer_frequency_days=40,
            last_watered_date=today - timedelta(days=6),  # Overdue by 1 day!
            last_fertilized_date=today - timedelta(days=20),
            date_added=today - timedelta(days=45),
            notes="Sensitive to direct sunlight. Droops slightly when thirsty."
        )

        # Plant 3: Snake Plant (Succulent, drought tolerant)
        p3 = Plant(
            user_id=demo_user.id,
            name="Study Desk Sansevieria",
            category="Succulent",
            species="Dracaena trifasciata",
            watering_frequency_days=14,
            fertilizer_frequency_days=60,
            last_watered_date=today - timedelta(days=5),
            last_fertilized_date=today - timedelta(days=10),
            date_added=today - timedelta(days=90),
            notes="Very hardy. Requires water only when soil is 100% dry."
        )

        # Plant 4: Golden Pothos
        p4 = Plant(
            user_id=demo_user.id,
            name="Balcony Trailing Pothos",
            category="Indoor",
            species="Epipremnum aureum",
            watering_frequency_days=7,
            fertilizer_frequency_days=30,
            last_watered_date=today - timedelta(days=7),  # Due today!
            last_fertilized_date=today - timedelta(days=32),
            date_added=today - timedelta(days=30),
            notes="Trailing down from balcony planter shelf."
        )

        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # Generate reminders
        for p in [p1, p2, p3, p4]:
            sync_plant_reminders(p)

        # Seed sample growth milestones for Monstera
        g1 = GrowthRecord(
            user_id=demo_user.id,
            plant_id=p1.id,
            observation_date=today - timedelta(days=50),
            height_cm=22.0,
            condition="Healthy",
            notes="Initial repotting into 10-inch planter with moss pole."
        )
        g2 = GrowthRecord(
            user_id=demo_user.id,
            plant_id=p1.id,
            observation_date=today - timedelta(days=20),
            height_cm=28.5,
            condition="Flourishing",
            notes="Two new fenestrated leaves unfurled completely."
        )
        g3 = GrowthRecord(
            user_id=demo_user.id,
            plant_id=p1.id,
            observation_date=today - timedelta(days=2),
            height_cm=33.0,
            condition="Flourishing",
            notes="Aerial roots attached firmly to moss pole."
        )
        db.session.add_all([g1, g2, g3])

        # Seed sample care history
        h1 = CareHistory(
            user_id=demo_user.id,
            plant_id=p1.id,
            plant_name=p1.name,
            activity_type="watering",
            activity_date=today - timedelta(days=4),
            activity_description=f"Watered {p1.name} with filtered room-temperature water.",
            completion_status="completed"
        )
        h2 = CareHistory(
            user_id=demo_user.id,
            plant_id=p1.id,
            plant_name=p1.name,
            activity_type="fertilizer",
            activity_date=today - timedelta(days=15),
            activity_description="Fed balanced 20-20-20 liquid houseplant food.",
            completion_status="completed"
        )
        db.session.add_all([h1, h2])

        # Seed initial notification
        n1 = Notification(
            user_id=demo_user.id,
            plant_id=p2.id,
            title=f"{p2.name} is Overdue for Watering!",
            message=f"Your {p2.name} was due for watering 1 day ago. Please check its soil.",
            notification_type="watering",
            is_read=False
        )
        db.session.add(n1)

        db.session.commit()
        print(f"Populated 4 sample plants, care reminders, and growth milestones for demo user.")
    else:
        print("Demo user already has plants.")
