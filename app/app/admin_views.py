from app import app
from flask import render_template

@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("admin/dashboard.html")
    #return "Admin dashboard"

@app.route("/admin/profile")
def admin_profile():
    return render_template("admin/profile.html")
    #return "Admin dashboard"