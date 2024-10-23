from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from app import app, db
from models import User, Advisor, Appointment, FAQ
from chatbot import process_message
from auth import authenticate_user
from datetime import datetime, timedelta
from functools import wraps
import logging
import traceback

# Configure logging
logging.basicConfig(filename='chatbot.log', level=logging.ERROR)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You must be an admin to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template('chat.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if authenticate_user(username, password):
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    message = request.form.get('message')
    try:
        if not message:
            raise ValueError("Empty message received")
        
        response = process_message(message)
        
        if "schedule an appointment with" in message.lower():
            advisor_name = message.split("with")[-1].strip()
            advisor = Advisor.query.filter(Advisor.name.ilike(f"%{advisor_name}%")).first()
            
            if advisor:
                appointment_date = datetime.now() + timedelta(days=7)
                new_appointment = Appointment(
                    user_id=current_user.id,
                    advisor_id=advisor.id,
                    date=appointment_date,
                    status='Scheduled'
                )
                db.session.add(new_appointment)
                db.session.commit()
                
                response += f"\n\nI've scheduled an appointment for you with {advisor.name} on {appointment_date.strftime('%Y-%m-%d %H:%M')}."
            else:
                response += f"\n\nI'm sorry, but I couldn't find an advisor named {advisor_name}."
        
        return jsonify({'response': response})
    except Exception as e:
        error_message = f"Error processing message: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_message)
        return jsonify({'error': 'An error occurred processing your message'}), 500

# Admin routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    faq_count = FAQ.query.count()
    advisor_count = Advisor.query.count()
    return render_template('admin/dashboard.html',
                         active_page='dashboard',
                         faq_count=faq_count,
                         advisor_count=advisor_count)

@app.route('/admin/calendar')
@admin_required
def admin_calendar():
    advisors = Advisor.query.all()
    appointments = Appointment.query.filter(
        Appointment.date >= datetime.now()
    ).order_by(Appointment.date).all()
    users = {user.id: user for user in User.query.all()}
    return render_template('admin/calendar.html',
                         active_page='calendar',
                         advisors=advisors,
                         appointments=appointments,
                         users=users)

@app.route('/admin/appointment/schedule', methods=['POST'])
@admin_required
def admin_schedule_appointment():
    try:
        date_str = request.form.get('date')
        appointment_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        
        new_appointment = Appointment(
            user_id=request.form.get('user_id', type=int),
            advisor_id=request.form.get('advisor_id', type=int),
            date=appointment_date,
            status='Scheduled'
        )
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/appointment/<int:appointment_id>/cancel', methods=['POST'])
@admin_required
def admin_cancel_appointment(appointment_id):
    try:
        appointment = Appointment.query.get_or_404(appointment_id)
        appointment.status = 'Cancelled'
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# [Previous routes remain unchanged...]
