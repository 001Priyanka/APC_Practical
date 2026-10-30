# BlogHub: Blogging and Skill Exploration Platform

BlogHub is a server-rendered web application built with Python and Django. It combines a blogging platform with an author skill-discovery network.

---

## Technology Stack

- **Backend**: Python 3.10+ / Django 5.1
- **Database**: MySQL 8.x via Django ORM and pure-Python `pymysql` driver (with SQLite temporary fallback)
- **Frontend**: Django Templates, Bootstrap 5.3, Bootstrap Icons, Custom CSS3, Vanilla JavaScript
- **Security & Config**: `python-dotenv`, CSRF protection, PBKDF2 password hashing, server-side image upload validation

---

## Project Structure

```
D:\PythonBlogProject\
├── .env                             # Local environment variables (git-ignored)
├── .env.example                     # Environment template with placeholders
├── .gitignore                       # Git ignore definitions
├── manage.py                        # Django administrative CLI
├── requirements.txt                 # Project dependencies
├── PROJECT_PLAN.md                  # Comprehensive architectural blueprint
├── README.md                        # Setup and run guide
├── config/                          # Main project package
│   ├── __init__.py                  # PyMySQL initialization
│   ├── asgi.py
│   ├── settings.py                  # Core configuration (Apps, DB, Media, Static)
│   ├── urls.py                      # Root URL routing
│   ├── validators.py                # Server-side image format & size validators
│   ├── views.py                     # Homepage view
│   └── wsgi.py
├── accounts/                        # User authentication and profile app
│   ├── admin.py                     # Profile and customized User admin
│   ├── apps.py
│   ├── models.py                    # Profile model & auto-provisioning signal
│   ├── tests.py                     # Profile model unit tests
│   ├── urls.py                      # /accounts/ routes
│   └── views.py
├── blogs/                           # Blog lifecycle and taxonomies app
│   ├── admin.py                     # Category, Tag, and Blog admin
│   ├── apps.py
│   ├── models.py                    # Category, Tag, and Blog models
│   ├── tests.py                     # Blog model & slug unit tests
│   ├── urls.py                      # /blogs/ routes
│   └── views.py
├── interactions/                    # Social features app
│   ├── admin.py                     # Comment, Like, and Bookmark admin
│   ├── apps.py
│   ├── models.py                    # Comment, Like, and Bookmark models
│   ├── tests.py                     # Interaction model constraints unit tests
│   ├── urls.py                      # /interactions/ routes
│   └── views.py
├── static/                          # Global static files
│   ├── css/style.css                # Custom visual styling
│   └── js/main.js                   # Client-side scripts
├── templates/                       # Master Django templates
│   ├── base.html                    # Master layout with responsive navbar & footer
│   └── home.html                    # Homepage hero and feature cards
└── media/                           # User-uploaded files (avatars, covers)
```

---

## Database Models Implemented

1. **`accounts.Profile`**
   - One-to-one relationship with Django's built-in `User`
   - Automatically provisioned via `post_save` signals
   - Fields: `bio`, `profile_image` (with size and format validation), `skills`, `interests`, timestamps

2. **`blogs.Category`**
   - High-level editorial classification
   - Fields: `name`, `slug` (auto-generated), `description`, timestamps

3. **`blogs.Tag`**
   - Keyword tagging for blogs
   - Fields: `name`, `slug` (auto-generated), timestamps

4. **`blogs.Blog`**
   - Core blog post entity
   - Fields: `author` (User FK), `title`, `slug` (unique, auto-deduplicating), `excerpt`, `content`, `cover_image` (validated), `category` (FK), `tags` (M2M), `status` (`draft` or `published`), timestamps
   - Helpers: `reading_time_minutes` (~200 words per minute)
   - Compound index: `['status', '-created_date']`

5. **`interactions.Comment`**
   - Community discussions on posts
   - Fields: `blog` (FK), `user` (FK), `content`, timestamps

6. **`interactions.Like`**
   - Post likes with strict unique constraint: **one like per user per blog**
   - Fields: `blog` (FK), `user` (FK), `created_date`

7. **`interactions.Bookmark`**
   - Saved posts with strict unique constraint: **one bookmark per user per blog**
   - Fields: `blog` (FK), `user` (FK), `created_date`

---

## Windows Setup & Execution Guide

### 1. Open PowerShell or Command Prompt
Open your terminal and navigate to the project directory:
```powershell
cd D:\PythonBlogProject
```

### 2. Activate Virtual Environment
The virtual environment is already created in `venv`. Activate it:
```powershell
# PowerShell:
.\venv\Scripts\Activate.ps1

# If script execution is restricted in PowerShell, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or Command Prompt (cmd):
venv\Scripts\activate.bat
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables (`.env`)
The project reads configurations from `.env`. A pre-configured `.env` is already present.

#### If using MySQL:
1. Ensure MySQL Server is installed and running (e.g. via MySQL Installer or XAMPP).
   To start the Windows MySQL service:
   ```powershell
   net start MySQL80
   ```
2. Create the database in MySQL:
   ```sql
   CREATE DATABASE bloghub_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. Update `.env` with your MySQL credentials:
   ```env
   DB_ENGINE=mysql
   DB_NAME=bloghub_db
   DB_USER=root
   DB_PASSWORD=your_actual_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   ```

#### If using SQLite (Temporary Fallback):
If MySQL is not yet installed or configured on your system, keep `DB_ENGINE=sqlite` in `.env`:
```env
DB_ENGINE=sqlite
```

### 5. Check Django Configuration
Run the Django system check:
```powershell
python manage.py check
```

### 6. Apply Database Migrations
Run migrations to set up the database tables:
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 7. Run Automated Tests
Verify that all 11 model unit tests pass:
```powershell
python manage.py test
```

### 8. Create Superuser (Admin Access)
```powershell
python manage.py createsuperuser
```

### 9. Start the Development Server
```powershell
python manage.py runserver
```
Open your browser and visit:
👉 **http://127.0.0.1:8000/** (Homepage)
👉 **http://127.0.0.1:8000/admin/** (Django Administration)
