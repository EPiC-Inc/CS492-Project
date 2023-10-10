from flask import render_template, url_for, session, request
from . import app, config
from .sql import db
from .auth import check_passwd

@app.route('/sql') # type: ignore
def test_sql():
    cursor = db.cursor()
    response = cursor.execute("getLogin 'admin@sms.com'")
    row = response.fetchone()
    while row:
        return str(row)
        row = cursor.fetchone()

@app.route('/')
def index():
    #TODO: If logged in, return dashboard
    # Otherwise, return the school homepage
    return render_template("front_page/index.html")

@app.route('/login', methods=["GET"])
def display_login_page():
    return render_template("admin/login.html", allowed_tabs=["login"], selected_tab="login")

@app.route('/login', methods=["POST"])
def login():
    #TODO: actually do the logging in
    form = request.form
    email = form.get('email', '').strip().lower()
    passwd = form.get('password', '')
    if (email == config.default_user.lower()) and ():
        #TODO: Check if the user is already in the database
        # Otherwise, check if the passwd is the default
        #    passwd and add the user to the database
        ...
    if check_passwd(passwd):
        return "YAY!"
    return "Not implemented", 501