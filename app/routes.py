from flask import render_template, url_for, session, request
from . import app, config

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
    email = form.get('email', '').lower()
    #passwd = 
    if (email == config.default_user.lower()) and ():
        #TODO: Check if the user is already in the database
        # Otherwise, check if the passwd is the default
        #    passwd and add the user to the database
        ...
    return "Not implemented", 501