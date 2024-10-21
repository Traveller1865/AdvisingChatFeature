from app import app, db
from models import User

def test_and_create_user():
    with app.app_context():
        try:
            # Check for existing users
            existing_users = User.query.all()
            if existing_users:
                print("Existing users:")
                for user in existing_users:
                    print(f"Username: {user.username}, Email: {user.email}")
                return

            # If no users exist, create a test user
            test_user = User(username="test_user", email="test@example.com")
            test_user.set_password("password123")
            db.session.add(test_user)
            db.session.commit()
            print("Test user created successfully.")
            print("Test user credentials:")
            print("Username: test_user")
            print("Password: password123")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            db.session.close()

if __name__ == "__main__":
    test_and_create_user()
