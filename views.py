from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app as app
from models import db, Appointment, ApplicantInformation, ApplicantPreferences, AdditionalInformation
from datetime import datetime
from werkzeug.utils import secure_filename
import os

# Create a blueprint for routes
main_blueprint = Blueprint('main', __name__)


@main_blueprint.route("/")
def home():
    return render_template("home.html")

@main_blueprint.route("/requirements")
def requirements():
    return render_template("requirements_page.html")

@main_blueprint.route("/appointment")
def appointment():
    return render_template("appointment.html")

@main_blueprint.route("/ca-info")
def ca_info():
    return render_template("ca_info.html")

@main_blueprint.route('/application', methods=['GET', 'POST'])
def application():
    if request.method == 'POST':
        try:
            applicant_info = ApplicantInformation(
                last_name=request.form['last_name'],
                first_name=request.form['first_name'],
                preferred_name=request.form.get('preferred_name'),
                pronouns=request.form['pronouns'],
                student_id=request.form['student_id'],
                current_hall=request.form['cur_residence'],
                current_room_number=request.form['cur_room_num'],
                current_email=request.form['email'],
                current_phone_number=request.form['phone_number'],
                returning_ca_or_new_ca=request.form['cur_position'],
                major_1=request.form['major_1'],
                major_2=request.form.get('major_2'),
                minor_1=request.form.get('minor_1'),
                minor_2=request.form.get('minor_2'),
                class_year=request.form['next_year_standing'],
                cumulative_gpa=float(request.form['gpa']),
                leadership_experience=request.form.getlist('prev_leadership')
            )

            applicant_preferences = ApplicantPreferences(
                student_id=request.form['student_id'],
                substance_free_housing_interest=int(request.form['substance_housing_interest']),
                healthy_colby_interest=int(request.form['healthy_housing_interest']),
                population_interest=request.form['pop_interest'],
                staff_interest={
                    "Alone": int(request.form['staff_interest_2']),
                    "With a Partner": int(request.form['staff_interest_1'])
                },
                illc_interest=int(request.form['intercultural_housing_interest'])
            )

            additional_info = AdditionalInformation(
                student_id=request.form['student_id'],
                why_ca=request.form['text_response_1'],
                additional_comments=request.form.get('add_info')
            )


            db.session.add(applicant_info)
            db.session.add(applicant_preferences)
            db.session.add(additional_info)
            db.session.commit()

            flash('Application submitted successfully!', 'success')
            return redirect(url_for('main.ca_info'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting application: {e}', 'danger')
            return redirect(url_for('main.application'))
    
    return render_template('application.html')

@main_blueprint.route("/UserHome")
def user_home():
    return render_template("UserHome.html")

@main_blueprint.route("/assessment")
def assessment():
    return render_template("assessment.html")

