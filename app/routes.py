from sre_parse import State
from unittest.mock import seal

from flask import flash, redirect, render_template, request, session, url_for

from . import app, config
from .api import search_for_account
from .auth import check_passwd, generate_passwd
from .sql import execute_db, query_db


@app.route('/')
def index():
    # If logged in, return appropriate dashboard
    # Otherwise, return the school homepage
    if session.get("logged_in"):
        role = session.get("role")
        if role == 1:
            return render_template("front_page/admin_dashboard.html", firstname=session.get("firstname"), allowed_tabs=["dashboard", "manage_accounts"], selected_tab="dashboard")
        if role == 2:
            return render_template("front_page/professor_dashboard.html")
        if role == 3:
            return render_template("front_page/student_dashboard.html")
    return render_template("front_page/index.html",  allowed_tabs=["login"])

@app.route("/admin/accounts", methods=["GET"])
def account_admin_page(results=None):
    action = request.args.get('action', '')
    if action.lower() == "edit":
        action = "Edit Existing Account"
    else:
        action = "Create New Account"

    roles = query_db("getAccountRoles")
    return render_template("admin/accounts.html", 
                           allowed_tabs=["dashboard", "manage_accounts"], selected_tab="manage_accounts",
                           roles=roles, action=action)

@app.route("/admin/accounts", methods=["POST"])
def modify_account():
    form = request.form
    if request.args.get("action", '').lower() == "new":
        email = form.get("email", '')
        # Check if a duplicate account exists
        if bool(query_db("getAccountDetail :email",
                        email=email
                        )):
            flash("An account with this email already exists", 'error')
            return redirect(url_for("account_admin_page"))

        form = dict(form) # Make it mutable
        password, hash = generate_passwd()
        form['password'], form['hash'] = password, hash

        if None: #TODO - validate form input
            flash("Please make sure the form is filled out correctly", 'error')
            return redirect(url_for("account_admin_page"))

        execute_db("insertAccountDetail :firstName, :lastName, :hash, :email, :role, :homeAddress, :secondHomeAddress, '', :city, :state, :zipCode",
                **form
                )
        flash("Account created! Credentials:", 'success')
        flash(f"Email: {email}", 'success')
        flash(f"Password: {password}", 'success')
        return redirect(url_for("account_admin_page"))

    if request.args.get("action", '').lower() == "edit":
        print(form)
        if form.get("to_find") is not None:
            return render_template("admin/accounts.html", 
                           allowed_tabs=["dashboard", "manage_accounts"], selected_tab="manage_accounts",
                           action='Edit Existing Account', results=search_for_account(form.get("to_find", '')),
                           roles=query_db("getAccountRoles"))

    flash("Unknown error. Please reload the page and try again", 'error')
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
        #NOTE: Validate role on sensitive operations.

        session['logged_in'] = True
        #TODO: Make this customizable
        account_details = query_db(f"getAccountDetail '{email}'")[0]
        session['role'] = account_details[3]
        session['firstname'] = account_details[1]
        return redirect(url_for("index"))

    # Case: invalid credentials
    flash("Invalid email or password.", 'error')
    return redirect(url_for("login"))
