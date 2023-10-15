from flask import flash, redirect, render_template, request, session, url_for

from . import app, config
from .auth import check_passwd
from .sql import db, execute_on_db


@app.route('/sql') # type: ignore #TEMP
def test_sql():
    cursor = db.cursor()
    response = cursor.execute("getLogin 'admin@sms.com'")
    row = response.fetchone()
    while row:
        return str(row)
        row = cursor.fetchone()

@app.route('/')
def index():
    # If logged in, return appropriate dashboard
    # Otherwise, return the school homepage
    if session.get("logged_in", False):
        role = session.get("role")
        if role == "Faculty Administrator":
            return render_template("front_page/admin_dashboard.html", allowed_tabs=["dashboard", "manage_accounts"], selected_tab="dashboard")
        if role == "Faculty Member":
            return render_template("front_page/professor_dashboard.html")
        if role == "Student":
            return render_template("front_page/student_dashboard.html")
    return render_template("front_page/index.html")

@app.route("/admin/accounts", methods=["GET"])
def account_admin_page():
    return render_template("admin/accounts.html", allowed_tabs=["dashboard", "manage_accounts"], selected_tab="manage_accounts")

@app.route("/admin/accounts", methods=["POST"])
def modify_account():
    return str(request.form)

@app.route('/login', methods=["GET"])
def display_login_page():
    return render_template("admin/login.html", allowed_tabs=["login"], selected_tab="login")

@app.route('/login', methods=["POST"])
def login():
    #TODO: actually do the logging in
    form = request.form
    email = form.get('email', '').strip().lower()
    passwd = form.get('password', '')
    if (email == config.default_user.lower()) and (False):
        #TODO: Check if the user is already in the database
        # Otherwise, check if the passwd is the default
        #    passwd and add the user to the database
        ...
    if check_passwd(email, passwd):
        # Assign role to the user
        #NOTE: These use Flask's secure cookies, which are tamper-resistent.
        #TODO: Validate role on sensitive operations.

        session['logged_in'] = True
        #TODO: Make this customizable
        session['role'] = execute_on_db(f"getAccountDetail '{email}'")[0][3]
        return redirect(url_for("index"))

    # Case: invalid credentials
    flash("Invalid email or password.")
    return redirect(url_for("login"))