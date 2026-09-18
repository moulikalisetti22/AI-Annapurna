import os
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, flash, g, redirect, render_template, request, session, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "foodbridge.db"
UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True, parents=True)

app = Flask(__name__)
app.config["SECRET_KEY"] = "foodbridge-demo-secret-key"
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)


def get_db():
    db = getattr(g, "db", None)
    if db is None:
        db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
        g.db = db
    return db


@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, "db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, full_name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, role TEXT NOT NULL, phone TEXT, village TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
    db.execute("CREATE TABLE IF NOT EXISTS donations (id INTEGER PRIMARY KEY AUTOINCREMENT, donor_id INTEGER NOT NULL, food_name TEXT NOT NULL, quantity TEXT NOT NULL, food_type TEXT NOT NULL, location TEXT NOT NULL, latitude REAL, longitude REAL, pickup_time TEXT, expiry_time TEXT, safety_note TEXT, image_url TEXT, status TEXT DEFAULT 'Available', is_demo INTEGER DEFAULT 1, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
    db.execute("CREATE TABLE IF NOT EXISTS requests (id INTEGER PRIMARY KEY AUTOINCREMENT, donation_id INTEGER NOT NULL, requester_id INTEGER NOT NULL, request_type TEXT DEFAULT 'ngo', status TEXT DEFAULT 'Pending', created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
    db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, volunteer_id INTEGER NOT NULL, donation_id INTEGER NOT NULL, pickup_location TEXT NOT NULL, drop_location TEXT NOT NULL, task_status TEXT DEFAULT 'Assigned', created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
    db.execute("CREATE TABLE IF NOT EXISTS notifications (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, message TEXT NOT NULL, type TEXT DEFAULT 'info', is_read INTEGER DEFAULT 0, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")

    existing_users = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing_users == 0:
        password_hash = generate_password_hash("password123")
        db.execute(
            "INSERT INTO users (full_name, email, password_hash, role, phone, village) VALUES (?, ?, ?, ?, ?, ?)",
            ("Asha Donor", "donor@foodbridge.in", password_hash, "donor", "9876543210", "Konduru")
        )
        db.execute(
            "INSERT INTO users (full_name, email, password_hash, role, phone, village) VALUES (?, ?, ?, ?, ?, ?)",
            ("Green Hope NGO", "ngo@foodbridge.in", password_hash, "ngo", "9123456780", "Peddapalli")
        )
        db.execute(
            "INSERT INTO users (full_name, email, password_hash, role, phone, village) VALUES (?, ?, ?, ?, ?, ?)",
            ("Ravi Volunteer", "volunteer@foodbridge.in", password_hash, "volunteer", "9988776655", "Sattenapalli")
        )
        db.execute(
            "INSERT INTO users (full_name, email, password_hash, role, phone, village) VALUES (?, ?, ?, ?, ?, ?)",
            ("Admin User", "admin@foodbridge.in", password_hash, "admin", "9000000000", "Head Office")
        )

        donor_id = db.execute("SELECT id FROM users WHERE email = ?", ("donor@foodbridge.in",)).fetchone()[0]
        ngo_id = db.execute("SELECT id FROM users WHERE email = ?", ("ngo@foodbridge.in",)).fetchone()[0]
        volunteer_id = db.execute("SELECT id FROM users WHERE email = ?", ("volunteer@foodbridge.in",)).fetchone()[0]

        db.execute(
            "INSERT INTO donations (donor_id, food_name, quantity, food_type, location, latitude, longitude, pickup_time, expiry_time, safety_note, image_url, status, is_demo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                donor_id,
                "Rice and Curry",
                "18 plates",
                "Cooked Meal",
                "Konduru Market",
                16.6230,
                80.2000,
                "18:30 Today",
                "2026-09-19 23:00:00",
                "Prepared within 4 hours; kept covered and sealed",
                "/static/uploads/demo-rice.jpg",
                "Available",
                1,
            )
        )
        db.execute(
            "INSERT INTO donations (donor_id, food_name, quantity, food_type, location, latitude, longitude, pickup_time, expiry_time, safety_note, image_url, status, is_demo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                donor_id,
                "Vegetable Biryani",
                "25 servings",
                "Cooked Meal",
                "Mangalagiri Road",
                16.4300,
                80.5400,
                "Tomorrow 9:00 AM",
                "2026-09-19 12:00:00",
                "Freshly cooked; no dairy added",
                "/static/uploads/demo-biryani.jpg",
                "Accepted",
                1,
            )
        )
        db.execute(
            "INSERT INTO donations (donor_id, food_name, quantity, food_type, location, latitude, longitude, pickup_time, expiry_time, safety_note, image_url, status, is_demo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                donor_id,
                "Fresh Bread",
                "30 loaves",
                "Bakery",
                "Nallapadu Junction",
                16.3100,
                80.4300,
                "Today 18:00",
                "2026-09-21 10:00:00",
                "Stored in hygienic conditions",
                "/static/uploads/demo-bread.jpg",
                "Available",
                1,
            )
        )

        donation_2_id = db.execute("SELECT id FROM donations WHERE food_name = ? ORDER BY id DESC LIMIT 1", ("Vegetable Biryani",)).fetchone()[0]
        donation_3_id = db.execute("SELECT id FROM donations WHERE food_name = ? ORDER BY id DESC LIMIT 1", ("Fresh Bread",)).fetchone()[0]

        db.execute("INSERT INTO requests (donation_id, requester_id, request_type, status) VALUES (?, ?, ?, ?)", (donation_2_id, ngo_id, "ngo", "Accepted"))
        db.execute("INSERT INTO requests (donation_id, requester_id, request_type, status) VALUES (?, ?, ?, ?)", (donation_3_id, ngo_id, "ngo", "Pending"))
        db.execute("INSERT INTO tasks (volunteer_id, donation_id, pickup_location, drop_location, task_status) VALUES (?, ?, ?, ?, ?)", (volunteer_id, donation_2_id, "Mangalagiri Road", "Green Hope NGO Center", "In Transit"))
        db.execute("INSERT INTO tasks (volunteer_id, donation_id, pickup_location, drop_location, task_status) VALUES (?, ?, ?, ?, ?)", (volunteer_id, donation_3_id, "Nallapadu Junction", "Vulnerable Family Shelter", "Assigned"))
        db.execute("INSERT INTO notifications (user_id, message, type, is_read) VALUES (?, ?, ?, ?)", (donor_id, "Your donation at Konduru Market has been accepted by Green Hope NGO.", "status", 0))
        db.execute("INSERT INTO notifications (user_id, message, type, is_read) VALUES (?, ?, ?, ?)", (volunteer_id, "New pickup assigned for bread donation from Nallapadu Junction.", "task", 0))

    db.commit()
    db.close()


@app.before_request
def load_user():
    session.setdefault("user_id", None)
    session.setdefault("user_role", None)


@app.context_processor
def inject_user():
    user = None
    if session.get("user_id"):
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    return {"user": user}


@app.route("/")
def index():
    db = get_db()
    stats = {
        "donations": db.execute("SELECT COUNT(*) FROM donations").fetchone()[0],
        "volunteers": db.execute("SELECT COUNT(*) FROM users WHERE role = 'volunteer'").fetchone()[0],
        "ngos": db.execute("SELECT COUNT(*) FROM users WHERE role = 'ngo'").fetchone()[0],
        "delivered": db.execute("SELECT COUNT(*) FROM donations WHERE status = 'Delivered'").fetchone()[0],
    }
    latest = db.execute("SELECT d.*, u.full_name AS donor_name FROM donations d JOIN users u ON u.id = d.donor_id ORDER BY d.id DESC LIMIT 3").fetchall()
    return render_template("index.html", stats=stats, latest=latest)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        donor_name = request.form.get("donor_name") or "Demo Donor"
        food_name = request.form.get("food_name")
        quantity = request.form.get("quantity")
        food_type = request.form.get("food_type")
        location = request.form.get("location")
        pickup_time = request.form.get("pickup_time")
        expiry_time = request.form.get("expiry_time")
        safety_note = request.form.get("safety_note")
        latitude = request.form.get("latitude") or 16.5
        longitude = request.form.get("longitude") or 80.5
        image_file = request.files.get("food_image")

        if not all([food_name, quantity, food_type, location, pickup_time, expiry_time]):
            flash("Please complete all required food donation fields.", "danger")
            return redirect(url_for("donate"))

        try:
            expiry_dt = datetime.strptime(expiry_time, "%Y-%m-%dT%H:%M")
        except ValueError:
            flash("Expiry date must be in a valid datetime format.", "danger")
            return redirect(url_for("donate"))

        if expiry_dt <= datetime.now():
            flash("Donation rejected: food is already expired or unsafe for distribution.", "danger")
            return redirect(url_for("donate"))

        file_name = "demo-food.jpg"
        if image_file and image_file.filename:
            safe_name = secure_filename(image_file.filename)
            file_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{safe_name}"
            image_file.save(os.path.join(app.config["UPLOAD_FOLDER"], file_name))

        db = get_db()
        donor_id = db.execute("SELECT id FROM users WHERE role = 'donor' ORDER BY id LIMIT 1").fetchone()[0]
        db.execute(
            "INSERT INTO donations (donor_id, food_name, quantity, food_type, location, latitude, longitude, pickup_time, expiry_time, safety_note, image_url, status, is_demo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (donor_id, food_name, quantity, food_type, location, latitude, longitude, pickup_time, expiry_dt.strftime("%Y-%m-%d %H:%M:%S"), safety_note or "Checked for freshness and safety", f"/static/uploads/{file_name}", "Available", 1),
        )
        db.commit()
        flash("Donation submitted successfully for review and matching.", "success")
        return redirect(url_for("find_food"))

    return render_template("donate.html")


@app.route("/find-food")
def find_food():
    db = get_db()
    donations = db.execute("SELECT d.*, u.full_name AS donor_name FROM donations d JOIN users u ON u.id = d.donor_id WHERE d.status != 'Delivered' ORDER BY d.id DESC").fetchall()
    return render_template("find_food.html", donations=donations)


@app.route("/volunteer")
def volunteer():
    db = get_db()
    tasks = db.execute(
        "SELECT t.*, u.full_name AS volunteer_name, d.food_name, d.location AS donation_location FROM tasks t JOIN users u ON u.id = t.volunteer_id JOIN donations d ON d.id = t.donation_id ORDER BY t.id DESC"
    ).fetchall()
    return render_template("volunteer.html", tasks=tasks)


@app.route("/ngo-dashboard")
def ngo_dashboard():
    db = get_db()
    requests = db.execute(
        "SELECT r.*, d.food_name, d.location, d.status AS donation_status FROM requests r JOIN donations d ON d.id = r.donation_id ORDER BY r.id DESC"
    ).fetchall()
    return render_template("ngo_dashboard.html", requests=requests)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return redirect(url_for("login"))
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_role"] = user["role"]
            flash("Login successful.", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid login credentials.", "danger")
        return redirect(url_for("login"))
    return render_template("auth.html", mode="login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")
        phone = request.form.get("phone")
        village = request.form.get("village")

        if not all([full_name, email, password, role]):
            flash("Please fill in all required registration fields.", "danger")
            return redirect(url_for("register"))

        db = get_db()
        existing = db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if existing:
            flash("An account with this email already exists.", "danger")
            return redirect(url_for("register"))

        db.execute(
            "INSERT INTO users (full_name, email, password_hash, role, phone, village) VALUES (?, ?, ?, ?, ?, ?)",
            (full_name, email, generate_password_hash(password), role, phone, village),
        )
        db.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("auth.html", mode="register")


@app.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    role = session.get("user_role")
    if role == "admin":
        return redirect(url_for("admin_dashboard"))
    if role == "ngo":
        return redirect(url_for("ngo_dashboard"))
    if role == "volunteer":
        return redirect(url_for("volunteer"))
    return redirect(url_for("donate"))


@app.route("/admin")
def admin_dashboard():
    db = get_db()
    user_count = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    donation_count = db.execute("SELECT COUNT(*) FROM donations").fetchone()[0]
    request_count = db.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
    volunteer_count = db.execute("SELECT COUNT(*) FROM users WHERE role = 'volunteer'").fetchone()[0]
    recent_donations = db.execute("SELECT d.*, u.full_name AS donor_name FROM donations d JOIN users u ON u.id = d.donor_id ORDER BY d.id DESC LIMIT 5").fetchall()
    notifications = db.execute("SELECT * FROM notifications ORDER BY id DESC LIMIT 5").fetchall()
    return render_template("admin_dashboard.html", user_count=user_count, donation_count=donation_count, request_count=request_count, volunteer_count=volunteer_count, recent_donations=recent_donations, notifications=notifications)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/api/donations")
def api_donations():
    db = get_db()
    donations = db.execute("SELECT d.*, u.full_name AS donor_name FROM donations d JOIN users u ON u.id = d.donor_id WHERE d.status != 'Delivered' ORDER BY d.id DESC").fetchall()
    items = [{
        "id": row["id"],
        "food_name": row["food_name"],
        "location": row["location"],
        "quantity": row["quantity"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "status": row["status"],
        "donor_name": row["donor_name"],
    } for row in donations]
    return jsonify(items)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
