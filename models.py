from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, email, is_admin=False):
        self.username = username
        self.email = email
        self.is_admin = is_admin

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(64))

    def __init__(self, question, answer, category):
        self.question = question
        self.answer = answer
        self.category = category

class Advisor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    department = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name, department, email):
        self.name = name
        self.department = department
        self.email = email

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    advisor_id = db.Column(db.Integer, db.ForeignKey('advisor.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Scheduled')

    def __init__(self, user_id, advisor_id, date, status='Scheduled'):
        self.user_id = user_id
        self.advisor_id = advisor_id
        self.date = date
        self.status = status
