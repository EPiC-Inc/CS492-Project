from flask import render_template, url_for, session
from . import app

@app.route('/')
def index():
    # TODO: If logged in, return dashboard
    # Otherwise, return the school homepage
    return render_template("front_page/index.html")

@app.route('/login', methods=["GET"])
def display_login_page():
    return render_template("admin/login.html", allowed_tabs=["login"])

@app.route('/login', methods=["POST"])
def login():
    #TODO: actually do the logging in
    return "Not implemented", 501