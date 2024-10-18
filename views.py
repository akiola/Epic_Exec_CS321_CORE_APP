from flask import Blueprint, render_template

# Create a blueprint for routes
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route("/")
def home():
    return "Welcome"

@main_blueprint.route("/signin")
def signin():
    return render_template("signin.html")