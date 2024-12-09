# from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from website import db

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.email}>'

class Appointment(db.Model):
    __tablename__ = 'appointment'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), db.ForeignKey('applicant_information.student_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    applicant = db.relationship('ApplicantInformation', back_populates='appointment')

    def __repr__(self):
        return f'<Appointment for {self.student_id} on {self.date} at {self.time}>'

class ApplicantInformation(db.Model):
    __tablename__ = 'applicant_information'
    

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    preferred_name = db.Column(db.String(100), nullable=True)
    pronouns = db.Column(db.String(50), nullable=False, default='N/A')
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    current_hall = db.Column(db.String(100), nullable=False)
    current_room_number = db.Column(db.String(20), nullable=False)
    current_email = db.Column(db.String(255), nullable=False)
    current_phone_number = db.Column(db.String(20), nullable=False)
    returning_ca_or_new_ca = db.Column(db.String(20), nullable=False)
    major_1 = db.Column(db.String(100), nullable=False)


    # edit to not show if not there
    major_2 = db.Column(db.String(100), nullable=True)
    minor_1 = db.Column(db.String(100), nullable=True)
    minor_2 = db.Column(db.String(100), nullable=True)


    class_year = db.Column(db.String(20), nullable=False)
    cumulative_gpa = db.Column(db.Float, nullable=False)


    # edit 
    leadership_experience = db.Column(db.PickleType, nullable=False)
    application_status = db.Column(db.String(50), default='Submitted', nullable=False)


    # fine content
    assessment_status = db.Column(db.String(50), default='Yet to Be Assessed', nullable=False)
    
    # Relationships
    preferences = db.relationship('ApplicantPreferences', backref='applicant', uselist=False)
    additional_info = db.relationship('AdditionalInformation', backref='applicant', uselist=False)
    appointment = db.relationship('Appointment', back_populates='applicant', uselist=False)
    assessment_form = db.relationship('AssessmentForm', back_populates='applicant', uselist=False)


    def rewrite_applicant_data(self) :

        rewrite_building = lambda value: (
                
            'Alfond Main St. Commons' if value == '0' else
            'Alfond Senior Apartments' if value == '1' else
            'Anthony' if value == '2' else
            'Averill' if value == '3' else
            'Coburn' if value == '4' else
            'Dana' if value == '5' else
            'Drummond' if value == '6' else
            'East' if value == '7' else
            'Foss' if value == '8' else
            'Goddard-Hodgkins' if value == '9' else
            'Heights' if value == '10' else
            'Johnson' if value == '11' else
            'Johnson Pond House 1' if value == '12' else
            'Johnson Pond House 2' if value == '13' else
            'Johnson Pond House 3' if value == '14' else
            'Johnson Pond House 4' if value == '15' else
            'Leonard' if value == '16' else
            'Marriner' if value == '17' else
            'Mary Low' if value == '18' else
            'Mitchell' if value == '19' else
            'Perkins-Wilson' if value == '20' else
            'Pierce' if value == '21' else
            'Piper' if value == '22' else
            'Roberts' if value == '23' else
            'Schpuf' if value == '24' else
            'Sturtevant' if value == '25' else
            'Taylor' if value == '26' else
            'Trewordy' if value == '27' else
            'West' if value == '28' else
            'Williams' if value == '29' else
            'Woodman' if value == '30' else
            '36 Mt.Merci' if value == '31' else
            'Hill House' if value == '32' else
            value

        )

        rewrite_ca_exp = lambda string : (

            'Applying for a new CA position' if string == '0' else
            'Applying for a returning CA position' if string == '1' else
            'ERROR IN APPLICANT DETAILS...'

        )

        rewrite_leadership_exp = lambda list: [

            'COOT Committee' if item == '0' else 
            'COOT Leader' if item == '1' else
            'Community Advisor' if item == '2' else
            'FLI Fellow' if item == '3' else
            'FLI Program Mentor (First Generation to College/Low Income Program)' if item == '4' else
            'International Student Buddy' if item == '5' else
            'International Student Fellow' if item == '6' else
            'Orientation Committee' if item == '7' else
            'Orientation Leader' if item == '8' else
            'No previous applicable experience' if item == '9' else
            'ERROR IN REWRITE_LEADERSHIP_EXP'
            for item in list

        ]

        rewritten = {

            # personal information
            'first_name' : self.first_name,
            'last_name' : self.last_name,
            'preferred_name' : self.preferred_name,
            'pronouns' : self.pronouns,
            'student_id' : self.student_id,
            'current_hall' : rewrite_building(self.current_hall),
            'current_room_number' : self.current_room_number,
            'current_email' : self.current_email,
            'current_phone_number' : self.current_phone_number,

            # academic information
            'major_1' : self.major_1,
            'major_2' : self.major_2,
            'minor_1' : self.minor_1,
            'minor_2' : self.minor_2,
            'class_year' : self.class_year,
            'cumulative_gpa' : self.cumulative_gpa,

            # ca experience
            'returning_ca_or_new_ca' : rewrite_ca_exp(self.returning_ca_or_new_ca),
            'leadership_experience' : rewrite_leadership_exp(self.leadership_experience),

            # application status
            'application_status' : self.application_status,
            'interview_status' : (self.get_interview_status()),
            'assessment_status' : self.assessment_status

        }

        return rewritten

    def get_interview_status(self):
        if self.appointment:
            return f"Scheduled for {self.appointment.date} at {self.appointment.time}"
        return "Yet To Schedule"

    def __repr__(self):
        return f'<ApplicantInformation {self.first_name} {self.last_name}>'

class ApplicantPreferences(db.Model):
    __tablename__ = 'applicant_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    substance_free_housing_interest = db.Column(db.Integer, nullable=False)
    healthy_colby_interest = db.Column(db.String(100), nullable=False)
    population_interest = db.Column(db.String(100), nullable=False)
    staff_interest = db.Column(db.PickleType, nullable=False) 
    illc_interest = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), db.ForeignKey('applicant_information.student_id'), nullable=False)

    def rewrite_preferences(self) :

        rewrite_int = lambda value : {

            1 : 'Not at all Interested (1)',
            2 : 'A Little Interested (2)',
            3 : 'Somewhat Interested (3)',
            4 : 'Interested (4)',
            5 : 'Very Interested (5)'

        }.get(value, 'ERROR IN PREFERENCE SUBMISSION')

        rewrite_string = lambda string : {

            '1' : 'Not at all Interested (1)',
            '2' : 'A Little Interested (2)',
            '3' : 'Somewhat Interested (3)',
            '4' : 'Interested (4)',
            '5' : 'Very Interested (5)'

        }.get(string, 'ERROR IN PREFERENCE SUBMISSION')

        rewrite_staff = lambda preferences : [
            f"Being a CA {condition[0].lower() + condition[1:]} : {rewrite_int(preference)}" 
            for condition, preference in preferences.items()
        ]        

        rewrite_pop = lambda string : {

            '0' : 'Highly interested in working with first year students (4)',
            '1' : 'Moderately interested in working with first year students (3)',
            '2' : 'Somewhat interested in working with first year students (2)',
            '3' : 'Not interested in working with first year students (1)'

        }.get(string, 'ERROR IN REWRITE_POP')

        rewritten = {
            'substance_free_housing_interest' : rewrite_int(self.substance_free_housing_interest),
            'healthy_colby_interest' : rewrite_string(self.healthy_colby_interest),
            'staff_interest_1' : (rewrite_staff(self.staff_interest))[0],
            'staff_interest_2' : (rewrite_staff(self.staff_interest))[1],
            'population_interest': rewrite_pop(self.population_interest),
            'illc_interest': rewrite_string(self.illc_interest)
        }

        return rewritten

class AdditionalInformation(db.Model):
    __tablename__ = 'additional_information'
    
    id = db.Column(db.Integer, primary_key=True)
    why_ca = db.Column(db.String(1000), nullable=False)
    additional_comments = db.Column(db.String(1000), nullable=True)
    student_id = db.Column(db.String(50), db.ForeignKey('applicant_information.student_id'), nullable=False)

class AssessmentForm(db.Model):
    __tablename__ = 'assessment_form'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(6), db.ForeignKey('applicant_information.student_id'), nullable=False)
    evaluator_name = db.Column(db.String(100), nullable=False) 
    
    q1_response = db.Column(db.Text, nullable=False)  
    q1_evaluation = db.Column(db.Integer, nullable=False)
    q2_response = db.Column(db.Text, nullable=False)
    q2_evaluation = db.Column(db.Integer, nullable=False)
    q3_response = db.Column(db.Text, nullable=False)
    q3_evaluation = db.Column(db.Integer, nullable=False)
    q4_response = db.Column(db.Text, nullable=False)
    q4_followup = db.Column(db.String(500))  
    q4_evaluation = db.Column(db.Integer, nullable=False)
    q5_response = db.Column(db.Text, nullable=False)
    q5_followup = db.Column(db.String(500)) 
    q5_evaluation = db.Column(db.Integer, nullable=False)
    q6_response = db.Column(db.Text, nullable=False)
    q6_followup = db.Column(db.String(500))  
    q6_evaluation = db.Column(db.Integer, nullable=False)
    
    # Logistical Questions
    study_abroad_plans = db.Column(db.String(100))  
    can_attend_training = db.Column(db.Boolean, nullable=False)
    candidate_questions = db.Column(db.Text) 
    
    # Evaluator's Comments
    perceived_strengths = db.Column(db.Text, nullable=False) 
    perceived_growth_areas = db.Column(db.Text, nullable=False)
    general_comments = db.Column(db.String(1000)) 
    hiring_recommendation = db.Column(db.String(50), nullable=False) 
    recommendation_rationale = db.Column(db.String(1000)) 
    
    # Relationship
    applicant = db.relationship('ApplicantInformation', back_populates='assessment_form')
