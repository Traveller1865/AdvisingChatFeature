from app import app, db
from models import FAQ

calendar_faqs = [
    {
        "question": "When is the first day of school?",
        "answer": "The first day of school for the Fall 2024 semester is September 3, 2024.",
        "category": "Academic Calendar"
    },
    {
        "question": "When is the last day of school?",
        "answer": "The last day of school for the Spring 2025 semester is May 15, 2025.",
        "category": "Academic Calendar"
    },
    {
        "question": "What are the important semester dates?",
        "answer": "Fall 2024: Sept 3 - Dec 20, 2024\nSpring 2025: Jan 13 - May 15, 2025",
        "category": "Academic Calendar"
    },
    {
        "question": "When are the registration deadlines?",
        "answer": "Fall 2024 registration deadline: August 15, 2024\nSpring 2025 registration deadline: January 5, 2025",
        "category": "Academic Calendar"
    },
    {
        "question": "When are the exam periods?",
        "answer": "Fall 2024 exams: December 13-20, 2024\nSpring 2025 exams: May 8-15, 2025",
        "category": "Academic Calendar"
    }
]

def add_calendar_faqs():
    with app.app_context():
        for faq in calendar_faqs:
            new_faq = FAQ(question=faq['question'], answer=faq['answer'], category=faq['category'])
            db.session.add(new_faq)
        db.session.commit()
        print("Calendar FAQs added successfully.")

if __name__ == "__main__":
    add_calendar_faqs()
