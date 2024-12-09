from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify,current_app as app
# from models import db, Appointment, ApplicantInformation, ApplicantPreferences, AdditionalInformation
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import logging
# from email_sender import send_application_confirmation_email, send_interview_confirmation_email
from flask_login import login_required
from sqlalchemy import or_, and_
from website import db
from .models import Appointment, ApplicantInformation, ApplicantPreferences, AdditionalInformation, AssessmentForm
from .email_sender import send_application_confirmation_email, send_interview_confirmation_email

# Create a blueprint for routes
main_blueprint = Blueprint('main', __name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@main_blueprint.route("/")
def home():
    return render_template("home.html")


@main_blueprint.route("/admin_fun")
def admin_fun():
    return render_template("admin_fun.html")


@main_blueprint.route("/requirements")
def requirements():
    return render_template("requirements_page.html")


@main_blueprint.route("/appointment")
def appointment():
    return render_template("appointment.html")


@main_blueprint.route("/ca_info")
def ca_info():
    return render_template("ca_info.html")

@main_blueprint.route("/assessment_form/<string:student_id>")
def assessment_form(student_id):
    applicant = ApplicantInformation.query.filter_by(student_id=student_id).first_or_404()
    assessment = AssessmentForm.query.filter_by(student_id=student_id).first()
    return render_template(
        "normal_assessment.html",
        applicant=applicant,
        assessment=assessment
    )


@main_blueprint.route("/submit_assessment/<string:student_id>", methods=["POST"])
def submit_assessment(student_id):
    assessment = AssessmentForm.query.filter_by(student_id=student_id).first()

    if assessment:
        assessment.evaluator_name = request.form.get('evaluator_name')
        assessment.q1_response = request.form.get('q1_response')
        assessment.q1_evaluation = int(request.form.get('q1_evaluation'))
        assessment.q2_response = request.form.get('q2_response')
        assessment.q2_evaluation = int(request.form.get('q2_evaluation'))
        assessment.q3_response = request.form.get('q3_response')
        assessment.q3_evaluation = int(request.form.get('q3_evaluation'))
        assessment.q4_response = request.form.get('q4_response')
        assessment.q4_followup = request.form.get('q4_followup')
        assessment.q4_evaluation = int(request.form.get('q4_evaluation'))
        assessment.q5_response = request.form.get('q5_response')
        assessment.q5_followup = request.form.get('q5_followup')
        assessment.q5_evaluation = int(request.form.get('q5_evaluation'))
        assessment.q6_response = request.form.get('q6_response')
        assessment.q6_followup = request.form.get('q6_followup')
        assessment.q6_evaluation = int(request.form.get('q6_evaluation'))
        assessment.study_abroad_plans = request.form.get('study_abroad_plans')
        assessment.can_attend_training = request.form.get('can_attend_training') == 'Yes'
        assessment.candidate_questions = request.form.get('candidate_questions')
        assessment.perceived_strengths = request.form.get('perceived_strengths')
        assessment.perceived_growth_areas = request.form.get('perceived_growth_areas')
        assessment.general_comments = request.form.get('general_comments')
        assessment.hiring_recommendation = request.form.get('hiring_recommendation')
        assessment.recommendation_rationale = request.form.get('recommendation_rationale')
    else:
        assessment = AssessmentForm(
            student_id=student_id,
            evaluator_name=request.form.get('evaluator_name'),
            q1_response=request.form.get('q1_response'),
            q1_evaluation=int(request.form.get('q1_evaluation')),
            q2_response=request.form.get('q2_response'),
            q2_evaluation=int(request.form.get('q2_evaluation')),
            q3_response=request.form.get('q3_response'),
            q3_evaluation=int(request.form.get('q3_evaluation')),
            q4_response=request.form.get('q4_response'),
            q4_followup=request.form.get('q4_followup'),
            q4_evaluation=int(request.form.get('q4_evaluation')),
            q5_response=request.form.get('q5_response'),
            q5_followup=request.form.get('q5_followup'),
            q5_evaluation=int(request.form.get('q5_evaluation')),
            q6_response=request.form.get('q6_response'),
            q6_followup=request.form.get('q6_followup'),
            q6_evaluation=int(request.form.get('q6_evaluation')),
            study_abroad_plans=request.form.get('study_abroad_plans'),
            can_attend_training=request.form.get('can_attend_training') == 'Yes',
            candidate_questions=request.form.get('candidate_questions'),
            perceived_strengths=request.form.get('perceived_strengths'),
            perceived_growth_areas=request.form.get('perceived_growth_areas'),
            general_comments=request.form.get('general_comments'),
            hiring_recommendation=request.form.get('hiring_recommendation'),
            recommendation_rationale=request.form.get('recommendation_rationale')
        )
        db.session.add(assessment)

    try:
        db.session.commit()
        return redirect(url_for('main.admin_home'))
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400 


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
                leadership_experience=request.form.getlist('prev_leadership'),
                application_status='Submitted'
            )

            applicant_preferences = ApplicantPreferences(
                student_id=request.form['student_id'],
                substance_free_housing_interest=int(
                    request.form['substance_housing_interest']),
                healthy_colby_interest=int(
                    request.form['healthy_housing_interest']),
                population_interest=request.form['pop_interest'],
                staff_interest={
                    "Alone": int(request.form['staff_interest_2']),
                    "With a Partner": int(request.form['staff_interest_1'])
                },
                illc_interest=int(
                    request.form['intercultural_housing_interest'])
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

            try:
                send_application_confirmation_email(request.form['email'])
                flash(
                    'Application submitted successfully! A confirmation email has been sent.', 'success')
            except Exception as e:
                logger.error(
                    f"Failed to send application confirmation email: {str(e)}")
                flash(
                    'Application submitted successfully! However, there was an issue sending the confirmation email.', 'warning')

            return redirect(url_for('main.ca_info'))

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error submitting application: {str(e)}")
            flash(f'Error submitting application. Please try again later.', 'danger')
            return redirect(url_for('main.application'))

    return render_template('application.html')


@login_required
@main_blueprint.route("/admin_homepage")
def admin_home():
    search_query = request.args.get('search', '').strip()

    if search_query:
        search_terms = search_query.split()

        if len(search_terms) > 1:
            applicants = ApplicantInformation.query.filter(
                or_(
                    and_(
                        ApplicantInformation.first_name.ilike(f'%{search_terms[0]}%'),
                        ApplicantInformation.last_name.ilike(f'%{search_terms[-1]}%')
                    ),
                    *[
                        or_(
                            ApplicantInformation.first_name.ilike(f'%{term}%'),
                            ApplicantInformation.last_name.ilike(f'%{term}%')
                        )
                        for term in search_terms
                    ]
                )
            ).all()
        else:
            applicants = ApplicantInformation.query.filter(
                or_(
                    ApplicantInformation.first_name.ilike(f'%{search_query}%'),
                    ApplicantInformation.last_name.ilike(f'%{search_query}%')
                )
            ).all()
    else:
        applicants = ApplicantInformation.query.all()

    applicants_data = []
    for applicant in applicants:
        appointment = Appointment.query.filter_by(
            student_id=applicant.student_id).first()
        interview_status = "Yet To Schedule"
        if appointment:
            interview_status = f"Scheduled for {appointment.date} at {appointment.time}"
        applicants_data.append({
            'first_name': applicant.first_name,
            'last_name': applicant.last_name,
            'student_id': applicant.student_id,
            'application_status': applicant.application_status,
            'interview_status': interview_status,
            'assessment_status': applicant.assessment_status
        })
    return render_template("admin_homepage.html", applicants=applicants_data, search_query=search_query)

@main_blueprint.route("/assessment/<string:student_id>")
def assessment(student_id):
    applicant = ApplicantInformation.query.filter_by(student_id=student_id).first_or_404()
    return render_template("normal_assessment.html", applicant=applicant)

@main_blueprint.route("/apptSubmit", methods=['POST'])
def appt_submit():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        date_str = request.form.get('apptDate')
        time_str = request.form.get('apptTime')

        applicant = ApplicantInformation.query.filter_by(
            student_id=student_id).first()

        if not applicant:
            flash(
                'No application found for this student ID. Please submit an application first.', 'error')
            return redirect(url_for('main.appointment'))

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time = datetime.strptime(time_str, '%H:%M').time()

            new_appointment = Appointment(
                student_id=student_id,
                date=date,
                time=time
            )
            db.session.add(new_appointment)
            db.session.commit()

            try:
                send_interview_confirmation_email(
                    applicant.current_email, f"{applicant.first_name} {applicant.last_name}", date_str, time_str)
                flash(
                    'Appointment scheduled successfully! A confirmation email has been sent.', 'success')
            except Exception as e:
                logger.error(
                    f"Failed to send interview confirmation email: {str(e)}")
                flash(
                    'Appointment scheduled successfully! However, there was an issue sending the confirmation email.', 'warning')

            return redirect(url_for('main.appointment'))
        except ValueError:
            flash('Invalid date or time format. Please try again.', 'error')
            return redirect(url_for('main.appointment'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error scheduling appointment: {str(e)}")
            flash(f'Error scheduling appointment. Please try again later.', 'danger')
            return redirect(url_for('main.appointment'))

    return redirect(url_for('main.appointment'))


@main_blueprint.route('/applicants')
def view_all_applicants():
    applicants = ApplicantInformation.query.all()
    applicants_data = []
    for applicant in applicants:
        appointment = Appointment.query.filter_by(
            student_id=applicant.student_id).first()
        interview_status = "Yet To Schedule"
        if appointment:
            interview_status = f"Scheduled for {appointment.date} at {appointment.time}"
        applicants_data.append({
            'first_name': applicant.first_name,
            'last_name': applicant.last_name,
            'student_id': applicant.student_id,
            'application_status': applicant.application_status,
            'interview_status': interview_status,
            'assessment_status': applicant.assessment_status
        })
    return render_template('admin_homepage.html', applicants=applicants_data)


@login_required
@main_blueprint.route('/view_application/<string:student_id>')
def view_application(student_id):
    applicant = (ApplicantInformation.query.filter_by(
        student_id=student_id).first_or_404()).rewrite_applicant_data()
    preferences = (ApplicantPreferences.query.filter_by(
        student_id=student_id).first()).rewrite_preferences()
    additional_info = AdditionalInformation.query.filter_by(
        student_id=student_id).first()
    return render_template('view_application.html', applicant=applicant, preferences=preferences, additional_info=additional_info)


@login_required
@main_blueprint.route('/assess_applicant/<string:student_id>', methods=['GET', 'POST'])
def assess_applicant(student_id):
    applicant = ApplicantInformation.query.filter_by(
        student_id=student_id).first_or_404()

    if request.method == 'POST':
        assessment = request.form.get('assessment')
        applicant.assessment_status = assessment
        db.session.commit()
        flash('Assessment updated successfully', 'success')
        return redirect(url_for('main.admin_home'))

    return render_template('assess_applicant.html', applicant=applicant)
