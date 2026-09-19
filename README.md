# FoodBridge – Smart Food Donation & Distribution System

FoodBridge is a modern, responsive website prototype for a rural development project that connects surplus food from donors with NGOs, volunteers, and recipients in need. It helps reduce food waste and hunger by matching food donations with nearby communities using simple interfaces, location-based awareness, and safety checks.

## Project Overview

- Objective: connect hotels, restaurants, function halls, and households with NGOs and volunteers.
- Target users: food donors, NGOs, volunteers, administrators, and recipients.
- Core features: registration, donation submission, request tracking, volunteer tasks, map-based matching, voice assistance, admin dashboard, and notifications.
- Stack: HTML, CSS, JavaScript, Flask, SQLite for demo, MySQL schema prepared for production use.

## Project Structure

- `app.py` — Flask backend and routing
- `static/css/style.css` — responsive styling theme
- `static/js/main.js` — frontend behavior and voice prompts
- `templates/` — all website pages
- `database/mysql_schema.sql` — MySQL schema for deployment
- `requirements.txt` — Python dependency list

## Features Included

- Separate login and registration flows for donors, NGOs, volunteers, and admin users.
- Donation form with food name, quantity, type, location, pickup time, expiry, safety notes, and image upload.
- Interactive map for food availability using Leaflet and OpenStreetMap.
- NGO request and volunteer task workflow.
- Admin dashboard with key stats and notifications.
- Telugu and English voice assistance using browser speech synthesis.
- Demo sample data for college presentation and local testing.
- Safety validation to avoid expired or unsafe food distribution.

## Local Setup

1. Create and activate a virtual environment:
   ```bash
   cd /workspaces/AI-Annapurna
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask application:
   ```bash
   python app.py
   ```

4. Open the site in a browser:
   https://foodbridge-connects.lovable.app/

## Demo Login Accounts

Use these credentials for quick testing:

- Donor: `donor@foodbridge.in` / `password123`
- NGO: `ngo@foodbridge.in` / `password123`
- Volunteer: `volunteer@foodbridge.in` / `password123`
- Admin: `admin@foodbridge.in` / `password123`

## MySQL Setup for Production Deployment

The schema file is located at `database/mysql_schema.sql`.

1. Create a MySQL database named `foodbridge`.
2. Import the SQL file:
   ```bash
   mysql -u root -p < database/mysql_schema.sql
   ```
3. Update the backend for MySQL integration if required for production deployment.

## Safety Rules for Demo Data

- Demo donations are clearly intended for presentation purposes.
- Unsafe or expired food is blocked by the form validation logic.
- The prototype is suitable for a college expo demonstration and should be used as a proof of concept rather than production-grade deployment.

## Notes

This project is a working functional prototype designed for a Project Expo presentation. The sample data is realistic and intentionally marked as demo content to distinguish it from real food donations.

