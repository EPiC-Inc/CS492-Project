from sre_parse import State
from flask import flash, redirect, render_template, request, session, url_for

from . import app, config
from .auth import check_passwd, generate_passwd
from .sql import db, query_db, execute

@app.route('/')
def index():
    # If logged in, return appropriate dashboard
    # Otherwise, return the school homepage
    if session.get("logged_in", False):
        role = session.get("role")
        if role == "Faculty Administrator":
            return render_template("front_page/admin_dashboard.html", firstname=session.get("firstname"), allowed_tabs=["dashboard", "manage_accounts"], selected_tab="dashboard")
        if role == "Faculty Member":
            return render_template("front_page/professor_dashboard.html")
        if role == "Student":
            return render_template("front_page/student_dashboard.html")
    return render_template("front_page/index.html",  allowed_tabs=["login"])

@app.route("/admin/accounts", methods=["GET"])
def account_admin_page():
    roles = query_db("getAccountRoles")
    return render_template("admin/accounts.html", 
                           allowed_tabs=["dashboard", "manage_accounts"], selected_tab="manage_accounts",
                           roles=roles)

@app.route("/admin/accounts", methods=["POST"])
def modify_account():
    #TODO - check if a duplicate account exists
    form = request.form
    first_name = form.get("firstName", '').replace("'", "''")
    last_name = form.get("lastName", '').replace("'", "''")
    email = form.get("email", '').replace("'", "''")
    role = form.get("role", '3').replace("'", "''")
    address_line_1 = form.get("homeAddress", '').replace("'", "''")
    address_line_2 = form.get("secondHomeAddress", '').replace("'", "''")
    state = form.get("state", '').replace("'", "''")
    city = form.get("city", '').replace("'", "''")
    zip_code = form.get("zipCode", '').replace("'", "''")
    password, hash = generate_passwd()

    if None: #TODO - validate form input
        flash("Please make sure the form is filled out correctly")
        return redirect(url_for("account_admin_page"))

    print(f"insertAccountDetail '{first_name}', '{last_name}', '{hash}', '{email}', '{role}', '{address_line_1}', '{address_line_2}', '', '{city}', '{state}', '{zip_code}'")
    execute(f"insertAccountDetail '{first_name}', '{last_name}', '{hash}', '{email}', '{role}', '{address_line_1}', '{address_line_2}', '', '{city}', '{state}', '{zip_code}'")
    flash("Account created! Credentials:", 'success')
    flash(f"Email: {email}", 'success')
    flash(f"Password: {password}", 'success')
    return redirect(url_for("account_admin_page"))

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
        account_details = query_db(f"getAccountDetail '{email}'")[0]
        session['role'] = account_details[3]
        session['firstname'] = account_details[1]
        return redirect(url_for("index"))

    # Case: invalid credentials
    flash("Invalid email or password.", 'error')
    return redirect(url_for("login"))
