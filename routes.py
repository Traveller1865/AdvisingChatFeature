from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app import app, db
from models import User, Advisor, Appointment
from chatbot import process_message
from auth import authenticate_user
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(filename='chatbot.log', level=logging.ERROR)

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
        logging.error(f"Error processing message: {str(e)}")
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
