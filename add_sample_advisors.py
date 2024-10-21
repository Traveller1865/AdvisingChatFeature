from app import app, db
from models import Advisor

sample_advisors = [
    {"name": "Dr. Jane Smith", "department": "Computer Science", "email": "jsmith@example.com"},
    {"name": "Prof. John Doe", "department": "Mathematics", "email": "jdoe@example.com"},
    {"name": "Dr. Emily Brown", "department": "Physics", "email": "ebrown@example.com"}
]

def add_sample_advisors():
    with app.app_context():
        for advisor in sample_advisors:
            new_advisor = Advisor(**advisor)
            db.session.add(new_advisor)
        db.session.commit()
        print("Sample advisors added successfully.")

if __name__ == "__main__":
    add_sample_advisors()
