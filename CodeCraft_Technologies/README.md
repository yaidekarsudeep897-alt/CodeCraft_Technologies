# CodeCraft Technologies

A mobile-friendly Flask portfolio and lead-generation website for a small web development and software business.

## Features
- Responsive home, services, projects, about and contact pages
- Service packages and starting-price guidance
- Project showcase with clear demo/prototype labels
- Contact inquiry form with validation and CSRF protection
- Saves inquiries to SQLite
- Optional email notifications via SMTP
- Flash success messages and custom 404 page
- No paid services required to run locally

## Requirements
Python 3.10 or newer is recommended.

## Run locally

### Windows
```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Open http://127.0.0.1:5000

Before deployment, edit `.env` and set a long random `SECRET_KEY`, set `FLASK_DEBUG=false`, and configure a production database if needed. Never upload `.env` or real customer data to a public repository.

## Email notifications (optional)
Fill in the `MAIL_*` and `INQUIRY_EMAIL` values in `.env`. For Gmail, use an app password where supported, not your normal account password. If email is not configured, form submissions still save to SQLite.

## Deployment notes
Use a Flask-compatible host, set environment variables in its dashboard, and use a persistent database/storage option. Free-host availability and terms can change. Test the deployed contact form and backups. This starter project does not include an admin dashboard; add authenticated access before building one so customer inquiries are not publicly exposed.

## Customise
- Edit text and prices in `templates/services.html`
- Edit sample portfolio cards in `templates/projects.html`
- Replace the placeholder email in `templates/contact.html`
- Update brand colours in `static/css/style.css`

## Important
The project cards are sample portfolio entries. Replace them with your actual work and only claim features that are implemented and tested. Prices are suggested starting prices, not quotes or guarantees.
