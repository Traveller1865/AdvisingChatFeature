from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from app import app, db
from models import User, Advisor, Appointment
from chatbot import process_message
from datetime import datetime, timedelta
import logging
import traceback

# Configure logging
logging.basicConfig(filename='chatbot.log', level=logging.ERROR)

@app.route('/')
@login_required
def index():
    return redirect(url_for('chat'))

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/chat/message', methods=['POST'])
@login_required
def chat_message():
    message = request.form.get('message')
    try:
        if not message:
            raise ValueError("Empty message received")
        
        response = process_message(message)
        
        # Check if the message contains an advisor name for scheduling
        if "schedule an appointment with" in message.lower():
            advisor_name = message.split("with")[-1].strip()
            advisor = Advisor.query.filter(Advisor.name.ilike(f"%{advisor_name}%")).first()
            
            if advisor:
                # Create a placeholder date for the appointment (1 week from now)
                appointment_date = datetime.now() + timedelta(days=7)
                appointment = Appointment(user_id=current_user.id, advisor_id=advisor.id, date=appointment_date)
                db.session.add(appointment)
                db.session.commit()
                
                response += f"\n\nI've scheduled an appointment for you with {advisor.name} on {appointment_date.strftime('%Y-%m-%d %H:%M')}. If you need to change this date, please contact the advising office."
            else:
                response += f"\n\nI'm sorry, but I couldn't find an advisor named {advisor_name}. Please check the advisor list and try again with the correct name."
        
        return jsonify({'response': response})
    except Exception as e:
        error_message = f"Error processing message: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_message)
        return jsonify({'error': 'An error occurred while processing your message'}), 500

@app.route('/log_error', methods=['POST'])
@login_required
def log_error():
    error_data = request.json
    if error_data and 'error' in error_data:
        logging.error(f"Client-side error: {error_data['error']}")
        return jsonify({'message': 'Error logged successfully'}), 200
    else:
        return jsonify({'error': 'Invalid error data'}), 400
