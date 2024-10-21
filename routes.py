from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app import app, db
from models import User, Advisor, Appointment
from chatbot import process_message
from auth import authenticate_user
from datetime import datetime
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
        return jsonify({'response': response})
    except Exception as e:
        logging.error(f"Error processing message: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your message'}), 500

@app.route('/schedule_appointment', methods=['POST'])
@login_required
def schedule_appointment():
    advisor_name = request.form.get('advisor')
    date_str = request.form.get('date')
    
    advisor = Advisor.query.filter_by(name=advisor_name).first()
    if not advisor:
        return jsonify({'error': 'Advisor not found'})
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    except ValueError:
        return jsonify({'error': 'Invalid date format'})
    
    appointment = Appointment(user_id=current_user.id, advisor_id=advisor.id, date=date)
    db.session.add(appointment)
    db.session.commit()
    
    return jsonify({'message': f'Appointment scheduled with {advisor_name} on {date_str}'})

@app.route('/log_error', methods=['POST'])
@login_required
def log_error():
    error_data = request.json
    if error_data and 'error' in error_data:
        logging.error(f"Client-side error: {error_data['error']}")
        return jsonify({'message': 'Error logged successfully'}), 200
    else:
        return jsonify({'error': 'Invalid error data'}), 400
