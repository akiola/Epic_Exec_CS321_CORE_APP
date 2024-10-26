from flask import Blueprint, render_template

# Create a blueprint for routes
main_blueprint = Blueprint('main', __name__)


@main_blueprint.route("/")
def home():
    return render_template("home.html")


@main_blueprint.route("/signin")
def signin():
    return render_template("signin.html")


@main_blueprint.route("/appointment")
def appointment():
    return render_template("appointment.html")

@main_blueprint.route("/ca-info")
def ca_info():
    return render_template("ca_info.html")
