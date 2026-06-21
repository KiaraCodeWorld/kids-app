# Running Brain Quest Locally

Brain Quest is a Django web app for kids (ages 7–10) covering math, vocabulary, spelling, and more.

## Prerequisites

- Python 3.10+ installed
- The `.venv` virtual environment already exists in the project root (it's checked in)

---

## Quick Start (Windows — recommended)

Double-click `run_app.bat` in the project folder. It will:
1. Activate the virtual environment
2. Kill any process already on port 8000
3. Start the Django dev server
4. Open `http://localhost:8000` in your browser

---

## Manual Start

### 1. Activate the virtual environment

**PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
.venv\Scripts\activate.bat
```

### 2. Install dependencies (first time only)

```powershell
pip install -r requirements.txt
```

### 3. Apply database migrations (first time only)

```powershell
python manage.py migrate
```

### 4. Start the server

```powershell
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## Environment Variables

Create a `.env` file in the project root (already exists locally — do **not** commit it):

```env
OPENROUTER_API_KEY=sk-or-v1-...     # Required for AI explanations and content generation
GOOGLE_CLIENT_ID=...                 # Optional: enables Google social login
GOOGLE_CLIENT_SECRET=...             # Optional: enables Google social login
```

The app runs without Google credentials — social login will simply be unavailable.

---

## Useful Management Commands

```powershell
# Generate quiz/content data
python manage.py generate_content

# Open Django admin (create a superuser first)
python manage.py createsuperuser
# then visit http://127.0.0.1:8000/admin
```

---

## Key URLs

| URL | What it is |
|-----|-----------|
| `http://localhost:8000/` | Home / Daily Mission dashboard |
| `http://localhost:8000/math-tricks/` | Math tricks & mental math page |
| `http://localhost:8000/admin/` | Django admin panel |

---

## Troubleshooting

**Port 8000 already in use:**
```powershell
# Find and kill the process
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**`django-allauth` import error after install:**
Make sure you're running inside the `.venv` — check with `where python` (should point to `.venv\Scripts\python.exe`).

**Database errors after pulling new code:**
```powershell
python manage.py migrate
```
