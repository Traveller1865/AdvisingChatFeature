from app import app, db
from models import Advisor

sample_advisors = [
    {"name": "Dr. Jane Smith", "department": "Computer Science", "email": "jsmith2024@example.com"},
    {"name": "Prof. John Doe", "department": "Mathematics", "email": "jdoe2024@example.com"},
    {"name": "Dr. Emily Brown", "department": "Physics", "email": "ebrown2024@example.com"}
]

def add_sample_advisors():
    with app.app_context():
        for advisor in sample_advisors:
            # Check if advisor with same email exists
            existing = Advisor.query.filter_by(email=advisor['email']).first()
            if not existing:
                new_advisor = Advisor(**advisor)
                db.session.add(new_advisor)
        try:
            db.session.commit()
            print("Sample advisors added successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding advisors: {str(e)}")

if __name__ == "__main__":
    add_sample_advisors()
