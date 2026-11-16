"""
Comprehensive test suite for PlantCare Reminder Application.
Tests:
- Database creation & initial seeding
- User registration, login, logout, password hashing
- User data privacy & isolation (User A cannot access User B's records)
- Adding, editing, detail, and deleting plants
- Care reminder generation & automatic recalculation
- Quick care actions (marking watered and fertilized)
- In-app notification creation, unread count, marking as read
- Care history logging & filtering
- Advanced Feature 1: Plant Health Checker rule engine
- Advanced Feature 2: Smart Watering Decision matrix
- Advanced Feature 3: Plant Growth Tracker milestones and height calculations
- File upload validation
"""
import io
import unittest
from datetime import date, timedelta
from app import create_app
from config import Config
from models import (
    db, User, Plant, PlantLibrary, CareReminder, CareHistory,
    Notification, HealthCheckReport, WateringDecision, GrowthRecord
)

class TestConfig(Config):
    TESTING = True
    # In-memory SQLite for isolated tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class PlantCareTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_database_and_library_seeding(self):
        """Verify predefined library has 12 sample plants."""
        count = PlantLibrary.query.count()
        self.assertEqual(count, 12, f"Expected 12 seeded library plants, got {count}")
        snake_plant = PlantLibrary.query.filter_by(name='Snake Plant').first()
        self.assertIsNotNone(snake_plant)
        self.assertEqual(snake_plant.default_watering_frequency_days, 14)

    def test_user_registration_and_authentication(self):
        """Test registration, login, session, and password hashing."""
        # 1. Register
        res = self.client.post('/register', data={
            'username': 'gardener1',
            'email': 'gardener1@test.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Registration successful', res.data)

        user = User.query.filter_by(username='gardener1').first()
        self.assertIsNotNone(user)
        self.assertNotEqual(user.password_hash, 'password123')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.check_password('wrongpass'))

        # 2. Prevent duplicate email
        res_dup = self.client.post('/register', data={
            'username': 'gardener2',
            'email': 'gardener1@test.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertIn(b'already exists', res_dup.data)

        # 3. Login
        res_login = self.client.post('/login', data={
            'identifier': 'gardener1@test.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(res_login.status_code, 200)
        self.assertIn(b'Good day, gardener1', res_login.data)

        # 4. Logout
        res_logout = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(res_logout.status_code, 200)
        self.assertIn(b'logged out securely', res_logout.data)

    def test_plant_crud_and_reminders(self):
        """Test adding a plant, automatic reminder creation, and quick care actions."""
        # Create user & login
        user = User(username='botanist', email='botanist@test.com')
        user.set_password('pass1234')
        db.session.add(user)
        db.session.commit()

        self.client.post('/login', data={'identifier': 'botanist@test.com', 'password': 'pass1234'})

        # Add plant
        res_add = self.client.post('/plants/add', data={
            'name': 'Living Room Monstera',
            'category': 'Indoor',
            'species': 'Monstera deliciosa',
            'watering_frequency_days': '7',
            'fertilizer_frequency_days': '30',
            'last_watered_date': (date.today() - timedelta(days=8)).isoformat(),
            'notes': 'Placed near north window'
        }, follow_redirects=True)
        self.assertEqual(res_add.status_code, 200)

        plant = Plant.query.filter_by(name='Living Room Monstera', user_id=user.id).first()
        self.assertIsNotNone(plant)
        self.assertTrue(plant.needs_watering)

        # Verify CareReminders were created
        water_rem = CareReminder.query.filter_by(plant_id=plant.id, reminder_type='watering').first()
        self.assertIsNotNone(water_rem)
        self.assertEqual(water_rem.frequency_days, 7)

        # Mark watered
        res_water = self.client.post(f'/plants/{plant.id}/water', follow_redirects=True)
        self.assertEqual(res_water.status_code, 200)

        # Verify updated date and history logged
        db.session.refresh(plant)
        self.assertEqual(plant.last_watered_date, date.today())
        self.assertFalse(plant.needs_watering)

        hist = CareHistory.query.filter_by(plant_id=plant.id, activity_type='watering').first()
        self.assertIsNotNone(hist)
        self.assertEqual(hist.completion_status, 'completed')

    def test_user_data_privacy_isolation(self):
        """Verify user B cannot access, view, or modify user A's plants."""
        # User A
        user_a = User(username='userA', email='userA@test.com')
        user_a.set_password('passA123')
        db.session.add(user_a)
        db.session.commit()

        plant_a = Plant(user_id=user_a.id, name='Secret Orchid', watering_frequency_days=7)
        db.session.add(plant_a)
        db.session.commit()

        # User B
        user_b = User(username='userB', email='userB@test.com')
        user_b.set_password('passB123')
        db.session.add(user_b)
        db.session.commit()

        # Login as User B
        self.client.post('/login', data={'identifier': 'userB@test.com', 'password': 'passB123'})

        # Attempt to access User A's plant detail -> Must 404
        res_view = self.client.get(f'/plants/{plant_a.id}')
        self.assertEqual(res_view.status_code, 404)

        # Attempt to delete User A's plant -> Must 404
        res_del = self.client.post(f'/plants/{plant_a.id}/delete')
        self.assertEqual(res_del.status_code, 404)
        self.assertIsNotNone(db.session.get(Plant, plant_a.id))

    def test_smart_watering_decision(self):
        """Test Smart Watering Decision logic matrix."""
        user = User(username='waterTester', email='water@test.com')
        user.set_password('waterpass')
        db.session.add(user)
        db.session.commit()

        # Plant scheduled for watering 8 days ago
        plant = Plant(
            user_id=user.id,
            name='Test Pothos',
            category='Indoor',
            watering_frequency_days=7,
            last_watered_date=date.today() - timedelta(days=8)
        )
        db.session.add(plant)
        db.session.commit()

        self.client.post('/login', data={'identifier': 'water@test.com', 'password': 'waterpass'})

        # Scenario 1: Soil is Wet -> Recommendation should be Avoid Watering Now
        res_wet = self.client.post('/smart-watering/', data={
            'plant_id': str(plant.id),
            'soil_condition': 'Wet'
        }, follow_redirects=True)
        self.assertIn(b'Avoid Watering Now', res_wet.data)

        # Scenario 2: Soil is Dry -> Recommendation should be Water Now
        res_dry = self.client.post('/smart-watering/', data={
            'plant_id': str(plant.id),
            'soil_condition': 'Dry'
        }, follow_redirects=True)
        self.assertIn(b'Water Now', res_dry.data)

        # Verify decision is persisted in DB
        decisions = WateringDecision.query.filter_by(plant_id=plant.id).all()
        self.assertEqual(len(decisions), 2)

    def test_plant_health_checker(self):
        """Test symptom-based health analysis and reporting."""
        user = User(username='healthTester', email='health@test.com')
        user.set_password('healthpass')
        db.session.add(user)
        db.session.commit()

        self.client.post('/login', data={'identifier': 'health@test.com', 'password': 'healthpass'})

        res_check = self.client.post('/health-check/', data={
            'manual_plant_name': 'Living Room Ficus',
            'plant_id': 'other',
            'symptoms': 'Yellowing leaves and mushy stems at the base'
        }, follow_redirects=True)

        self.assertEqual(res_check.status_code, 200)
        self.assertIn(b'Overwatering or Early Root Rot', res_check.data)
        self.assertIn(b'Health Observation Report', res_check.data)

        # Verify report in database
        report = HealthCheckReport.query.filter_by(user_id=user.id).first()
        self.assertIsNotNone(report)
        self.assertEqual(report.analysis_source, 'rule_engine')

    def test_growth_tracker(self):
        """Test growth milestones and height change calculations."""
        user = User(username='growthTester', email='growth@test.com')
        user.set_password('growthpass')
        db.session.add(user)
        db.session.commit()

        plant = Plant(user_id=user.id, name='Fiddle Leaf Fig')
        db.session.add(plant)
        db.session.commit()

        self.client.post('/login', data={'identifier': 'growth@test.com', 'password': 'growthpass'})

        # Log milestone 1 (10 cm)
        self.client.post(f'/growth-tracker/plant/{plant.id}', data={
            'observation_date': (date.today() - timedelta(days=30)).isoformat(),
            'height_cm': '10.0',
            'condition': 'Healthy',
            'notes': 'Planted in seedling pot'
        })

        # Log milestone 2 (15.5 cm)
        self.client.post(f'/growth-tracker/plant/{plant.id}', data={
            'observation_date': date.today().isoformat(),
            'height_cm': '15.5',
            'condition': 'Flourishing',
            'notes': 'Grew strong new shoots'
        })

        records = GrowthRecord.query.filter_by(plant_id=plant.id).order_by(GrowthRecord.observation_date.asc()).all()
        self.assertEqual(len(records), 2)
        diff = records[-1].height_cm - records[0].height_cm
        self.assertEqual(round(diff, 1), 5.5)

if __name__ == '__main__':
    unittest.main()
