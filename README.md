# Plant Care Reminder Application 🌱
> **A Comprehensive College Project Backend & Responsive Web Application**

A full-stack Python Flask web application designed to help plant owners manage their personal plant collections, receive automated watering and fertilizer schedule reminders, view a visual care calendar, evaluate plant health symptoms using an automated botanical rule engine, calculate smart watering decisions based on observed soil conditions, and track plant growth progression over time.

---

## 🛠️ Technology Stack

* **Backend Framework:** Python 3.12 with Flask
* **Database & ORM:** SQLite 3 with Flask-SQLAlchemy
* **Authentication:** Flask-Login with secure session cookies
* **Password Hashing:** Werkzeug security (`generate_password_hash`, `check_password_hash`)
* **Image Processing:** Python Pillow (PIL) with MIME verification and secure UUID filenames
* **Frontend:** Responsive HTML5, Tailwind CSS, FontAwesome 6, and Vanilla JavaScript
* **Development Environment:** Visual Studio Code (Windows PowerShell / CMD / Bash)

> **No Hardware / IoT Required:** All plant conditions, watering records, and soil moisture states are entered manually by users without sensors or microcontrollers.

---

## 📋 Complete Feature Breakdown

1. **User Authentication & Privacy:**
   - User registration with duplicate email/username prevention
   - Secure login & logout with "remember me" session cookies
   - Forgot password & password reset workflow
   - Complete user data isolation (strict foreign keys and cascading deletion)
2. **Personalized Dashboard:**
   - Real-time dynamic count of total plants
   - Warning list of plants requiring watering today or overdue
   - Upcoming fertilizer reminders
   - Today's care tasks with one-click completion
   - Recent notifications & growth updates with quick-action shortcuts
3. **Plant Management (Add, Edit, Detail, Delete):**
   - Record plant name, category (Indoor, Outdoor, Succulent, Flowering, Herb, Foliage), species, notes, and photos
   - Configurable care schedules: watering frequency (days) and fertilizer frequency (days)
   - Search by name/species and filter collection by plant category
4. **Predefined Plant Library:**
   - Pre-seeded with 12 common indoor and outdoor plants (Monstera, Snake Plant, Peace Lily, Pothos, Spider Plant, Aloe Vera, ZZ Plant, Basil, Jade, Rubber Plant, Rose, Fiddle Leaf Fig)
   - Comprehensive botanical care guides (watering, sunlight, soil, fertilizer, instructions)
   - One-click "+ Add to My Plants" button that prefills the Add Plant form
5. **Watering & Fertilizer Reminders:**
   - Automatically calculates next scheduled watering and fertilizer dates
   - Identifies active, due-today, and overdue care tasks
   - One-click "Mark Watered" or "Mark Fertilized" actions that update the plant's schedule and log the activity
6. **Care Calendar:**
   - Interactive monthly calendar grid with month navigation (< Month >)
   - Color-coded care events (Blue for watering, Purple for fertilizer, Green for completed, Red for overdue)
   - Daily event breakdown with direct task completion buttons
7. **Garden Notifications:**
   - In-app notification bell with live unread counter badge
   - Auto-generated notifications for due-today and overdue care tasks
   - Desktop browser notification permission support via JavaScript Notification API
8. **Care History:**
   - Comprehensive, filterable audit log of completed care tasks
   - Filter by activity type (watering, fertilizing, repotting, pruning) or by specific plant
9. **User Profile & Settings:**
   - Edit username, email, and upload profile avatar
   - Toggle notification preferences (Email summaries and Browser desktop alerts)
   - Secure password update form
10. **Advanced Feature 1: Plant Health Checker:**
    - Upload a photograph of affected leaves or stems
    - Select symptoms from quick-select symptom chips or enter custom descriptions
    - Rule-based botanical pathology engine evaluates symptoms (overwatering, underwatering, spider mites, etiolation, fungal leaf spots, nutrient deficiencies)
    - Provides likely causes, actionable step-by-step recovery steps, and educational botanical disclaimers
11. **Advanced Feature 2: Smart Watering Decision:**
    - Select a plant from your garden
    - Report observed soil condition: **Dry**, **Slightly Moist**, or **Wet**
    - The backend calculates a decision: **Water Now**, **Wait and Check Later**, or **Avoid Watering Now** with a detailed explanation
    - Logs decisions to the database for historical review
12. **Advanced Feature 3: Plant Growth Tracker:**
    - Log milestone observations over time with dates, height in cm, condition, and photos
    - Chronological timeline gallery
    - Side-by-side photo comparison of the first vs. latest milestone
    - Automatic calculation of cumulative height growth (e.g. `+5.5 cm`)

---

## 📁 Project Structure

```text
PlantCare/
├── app.py                      # Application factory, extensions init, blueprint registry
├── config.py                   # Configuration (Secret key, SQLite database URI, upload paths)
├── requirements.txt            # Python dependencies
├── seed_data.py                # Pre-seeded botanical library of 12 common plants
├── populate_demo_data.py       # Seeds default student account and sample plants
├── test_app.py                 # Automated unit and integration test suite (7 tests)
├── .env                        # Local environment variables
├── .env.example                # Example environment template
├── .gitignore                  # Git ignore rules for venv, instance DB, and uploads
│
├── models/                     # SQLAlchemy Models (9 Database Entities)
│   ├── __init__.py             # Database instance export
│   ├── user.py                 # User model with Werkzeug password hashing
│   ├── plant.py                # Plant collection model
│   ├── library.py              # PlantLibrary botanical reference model
│   ├── reminder.py             # CareReminder schedule model
│   ├── history.py              # CareHistory activity audit log
│   ├── notification.py         # Notification alert model
│   ├── health.py               # HealthCheckReport diagnostic model
│   ├── watering.py             # WateringDecision evaluation log
│   └── growth.py               # GrowthRecord photo and height model
│
├── routes/                     # Modular Blueprints
│   ├── auth.py                 # /login, /register, /logout, /forgot-password
│   ├── dashboard.py            # /dashboard summary view
│   ├── plants.py               # /plants CRUD and quick care actions
│   ├── library.py              # /library botanical catalog
│   ├── reminders.py            # /reminders schedule lists
│   ├── calendar.py             # /calendar interactive monthly planner
│   ├── notifications.py        # /notifications alerts & unread counter
│   ├── history.py              # /history activity log
│   ├── profile.py              # /profile user settings
│   ├── health_checker.py       # /health-check diagnosis engine
│   ├── smart_watering.py       # /smart-watering soil logic
│   └── growth_tracker.py       # /growth-tracker milestone gallery
│
├── services/                   # Core Business Logic
│   ├── reminder_service.py     # Date calculation and reminder synchronization
│   ├── notification_service.py # Overdue & due-today alert generator
│   ├── watering_service.py     # Soil moisture decision matrix
│   ├── health_analysis_service.py # Symptom-based pathology engine
│   └── upload_service.py       # Pillow image validation and secure storage
│
├── templates/                  # Jinja2 HTML Templates
│   ├── base.html               # Shared layout, navbar, notifications badge, footer
│   ├── dashboard.html          # Main dashboard
│   ├── auth/                   # login.html, register.html, forgot_password.html
│   ├── plants/                 # index.html, add.html, detail.html, edit.html
│   ├── library/                # index.html, detail.html
│   ├── reminders/              # index.html
│   ├── calendar/               # index.html
│   ├── notifications/          # index.html
│   ├── history/                # index.html
│   ├── profile/                # index.html
│   ├── health/                 # index.html, report.html, history.html
│   ├── watering/               # index.html, history.html
│   └── growth/                 # index.html, timeline.html
│
├── static/                     # Static CSS, JS, and Assets
│   ├── css/main.css
│   └── js/
├── uploads/                    # User-uploaded images (plants, health, growth, profiles)
└── instance/
    └── plantcare.db            # Persistent SQLite database
```

---

## 🚀 Step-by-Step Setup & Running Guide (Windows / VS Code)

### 1. Open Project in VS Code
Open the project directory in Visual Studio Code:
```powershell
code "C:\Users\SHIVSHAKTI C P\Desktop\keshav"
```

### 2. Activate Virtual Environment
Open a terminal in VS Code (`Ctrl + ~`) and activate the virtual environment:
```powershell
.\venv\Scripts\Activate.ps1
```
*(If PowerShell displays an execution policy warning, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first).*

### 3. Run the Application
Start the Flask development server:
```powershell
python app.py
```
You will see:
```text
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 4. Open in Your Browser
Open your browser and navigate to:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🔑 Pre-Configured Demo Account

You can register a new account anytime, or log in immediately using the pre-seeded demo user:

* **Username / Email:** `demo_student` (or `demo@college.edu`)
* **Password:** `plantcare123`

The demo account already contains 4 sample plants (*Monstera, Peace Lily, Sansevieria, and Pothos*), active reminders, growth records, and care history.

---

## 🧪 Running Automated Tests

To verify that all 7 core modules, database models, reminder calculations, and security isolation tests pass:

```powershell
python test_app.py
```

Expected result:
```text
.......
Ran 7 tests in 1.391s
OK
```

---

## 🛡️ Security & Privacy Compliance

* **Password Hashing:** Passwords are never stored in plain text; salted hashes are generated via PBKDF2/SHA256 through Werkzeug.
* **Session Protection:** Sensitive endpoints require authentication via Flask-Login `@login_required`.
* **User Isolation:** All database queries strictly filter by `user_id == current_user.id`. Changing URLs or record IDs will result in a `404 Not Found` response.
* **File Upload Verification:** Uploaded files are validated through Pillow to verify genuine image headers and prevent executable or polyglot uploads. Filenames are randomized with UUIDs.
