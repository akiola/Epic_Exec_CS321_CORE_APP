import pytest
from flask import url_for
from website.models import ApplicantInformation

@pytest.mark.parametrize('student_id, expected_status', [
    ('existing_id', 200),
    ('non_existing_id', 404)
])
def test_assessment_page(client, db, app_context, student_id, expected_status):
    if student_id == 'existing_id':
        applicant = ApplicantInformation(
            last_name = "Doe",
            first_name = "John",
            preferred_name = "Johnny",
            pronouns = "he/him",
            current_hall = '0',
            current_room_number='101',
            current_phone_number='1234567890',
            current_email='test@example.com',
            application_status='Submitted',
            assessment_status='Yet to Be Assessed',
            returning_ca_or_new_ca = "0",
            major_1 = "CS",
            class_year = "Sophomore",
            cumulative_gpa = 3.9,
            leadership_experience = [0, 1]
        )
        db.session.add(applicant)
        db.session.commit()

    response = client.get(url_for('main.view_application', student_id = student_id))
    assert response.status_code == expected_status

    if expected_status == 200:
        assert b"Assessment" in response.data

