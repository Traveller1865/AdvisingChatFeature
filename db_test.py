from app import app, db
from models import User, FAQ, Advisor, Appointment

def test_db_connection():
    with app.app_context():
        try:
            # Try to create all tables
            db.create_all()
            print("Database tables created successfully.")

            # Try to add a test user
            test_user = User(username="test_user", email="test@example.com")
            test_user.set_password("password123")
            db.session.add(test_user)
            db.session.commit()
            print("Test user added successfully.")

            # Query the user to verify
            queried_user = User.query.filter_by(username="test_user").first()
            if queried_user:
                print(f"Test user retrieved: {queried_user.username}")
            else:
                print("Failed to retrieve test user.")

            # Clean up
            db.session.delete(test_user)
            db.session.commit()
            print("Test user removed.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            db.session.close()

if __name__ == "__main__":
    test_db_connection()
