# -*- coding: utf-8 -*-
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import openpyxl
from datetime import datetime

# --- Basic Flask App Setup ---
app = Flask(__name__)

# --- Configuration ---
# Database Configuration (from environment variable set by Render)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.environ.get("SECRET_KEY", "your_default_secret_key") # Add a SECRET_KEY to your Render env variables for session management

# Upload folder (Render uses an ephemeral filesystem, consider cloud storage for persistent uploads)
# For now, this will work for temporary uploads during a session if needed by your app logic.
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads_prod")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Path for JSON data (if used by your app, ensure this path is writable or use a database)
NEXTJS_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports_data_final.json")

db = SQLAlchemy(app)

# --- Database Models ---
# IMPORTANT: Define your SQLAlchemy database models here.
# Example (replace with your actual models from your original main.py):
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

class FitnessData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    activity_type = db.Column(db.String(100), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    calories_burned = db.Column(db.Integer, nullable=True)
    activity_date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    user = db.relationship("User", backref=db.backref("fitness_data", lazy=True))

    def __repr__(self):
        return f"<FitnessData {self.activity_type} on {self.activity_date}>"

# --- Routes ---
# IMPORTANT: Define your Flask routes (endpoints) here.
# Example (replace with your actual routes from your original main.py):

@app.route("/")
def home():
    # Replace with your actual home page logic
    return "Welcome to the Fitness Data Manager! Please define your routes."

@app.route("/login", methods=["GET", "POST"])
def login():
    # IMPORTANT: Implement your login logic here
    # This is a placeholder
    if request.method == "POST":
        # username = request.form.get("username")
        # password = request.form.get("password")
        # user = User.query.filter_by(username=username).first()
        # if user and user.password == password: # Replace with secure password checking
        #     session["user_id"] = user.id
        #     flash("Logged in successfully!", "success")
        #     return redirect(url_for("dashboard")) # Example redirect
        # else:
        #     flash("Invalid credentials", "danger")
        pass
    return render_template("login.html") # Make sure you have this template or remove

@app.route("/data_entry", methods=["GET", "POST"])
def data_entry():
    # IMPORTANT: Implement your data entry logic here
    # This is a placeholder
    # if "user_id" not in session:
    #     return redirect(url_for("login"))
    if request.method == "POST":
        # activity_type = request.form.get("activity_type")
        # ... (get other form data)
        # new_data = FitnessData(user_id=session["user_id"], ...)
        # db.session.add(new_data)
        # db.session.commit()
        # flash("Data added successfully!", "success")
        # return redirect(url_for("data_entry"))
        pass
    return render_template("data_entry.html") # Make sure you have this template or remove

# --- Helper function to create tables (optional, Render might need this to be run differently or via migrations) ---
# You might need to run this once manually or adapt it for Render if tables are not created.
# Consider using Flask-Migrate for database migrations in a production environment.

# The following is NOT run by Gunicorn. Gunicorn directly imports the 'app' object.
# If you need to create tables, you might do it via a one-off job in Render 
# or by ensuring your Render `DATABASE_URL` points to an already initialized database.

# To initialize the database locally (if needed before first Render deploy or for local testing):
# from flask_sqlalchemy import inspect
# def create_tables_if_not_exist():
#     with app.app_context():
#         inspector = inspect(db.engine)
#         if not inspector.has_table("user") or not inspector.has_table("fitness_data"):
#             print("Creating database tables...")
#             db.create_all()
#             print("Database tables created.")
#         else:
#             print("Database tables already exist.")

# if __name__ == "__main__":
#     # create_tables_if_not_exist() # Uncomment to create tables locally if they don't exist
#     # IMPORTANT: For Render, Gunicorn runs the app. The host and port below are for local dev only.
#     # Render will set the PORT environment variable.
#     port = int(os.environ.get("PORT", 5003)) # Default to 5003 for local dev if PORT not set
#     app.run(host="0.0.0.0", port=port, debug=True) # debug=True for local dev only

# Ensure the 'app' object is available for Gunicorn
# No app.run() here when Gunicorn is used for production.

