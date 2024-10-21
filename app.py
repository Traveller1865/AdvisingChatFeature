import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a_secure_secret_key"

# Use an absolute path for the database file
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, 'instance', 'faq.db')
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    try:
        import models
        db.create_all()
        print("Database tables created successfully.")
    except Exception as e:
        print(f"An error occurred while creating database tables: {str(e)}")

from auth import login_manager
login_manager.init_app(app)

import routes

if __name__ == "__main__":
    print(f"Database path: {db_path}")
    app.run(host="0.0.0.0", port=5000)
