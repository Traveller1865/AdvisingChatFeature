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

@app.route('/admin/faqs')
@admin_required
def admin_faqs():
    faqs = FAQ.query.all()
    return render_template('admin/faqs.html', active_page='faqs', faqs=faqs)

@app.route('/admin/advisors')
@admin_required
def admin_advisors():
    advisors = Advisor.query.all()
    return render_template('admin/advisors.html', active_page='advisors', advisors=advisors)

# FAQ CRUD operations
@app.route('/admin/faq/add', methods=['POST'])
@admin_required
def admin_add_faq():
    try:
        new_faq = FAQ(
            question=request.form['question'],
            answer=request.form['answer'],
            category=request.form['category']
        )
        db.session.add(new_faq)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/faq/<int:faq_id>')
@admin_required
def admin_get_faq(faq_id):
    faq = FAQ.query.get_or_404(faq_id)
    return jsonify({
        'id': faq.id,
        'question': faq.question,
        'answer': faq.answer,
        'category': faq.category
    })

@app.route('/admin/faq/<int:faq_id>/edit', methods=['POST'])
@admin_required
def admin_edit_faq(faq_id):
    try:
        faq = FAQ.query.get_or_404(faq_id)
        faq.question = request.form['question']
        faq.answer = request.form['answer']
        faq.category = request.form['category']
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/faq/<int:faq_id>/delete', methods=['POST'])
@admin_required
def admin_delete_faq(faq_id):
    try:
        faq = FAQ.query.get_or_404(faq_id)
        db.session.delete(faq)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

# Advisor CRUD operations
@app.route('/admin/advisor/add', methods=['POST'])
@admin_required
def admin_add_advisor():
    try:
        new_advisor = Advisor(
            name=request.form['name'],
            department=request.form['department'],
            email=request.form['email']
        )
        db.session.add(new_advisor)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/advisor/<int:advisor_id>')
@admin_required
def admin_get_advisor(advisor_id):
    advisor = Advisor.query.get_or_404(advisor_id)
    return jsonify({
        'id': advisor.id,
        'name': advisor.name,
        'department': advisor.department,
        'email': advisor.email
    })

@app.route('/admin/advisor/<int:advisor_id>/edit', methods=['POST'])
@admin_required
def admin_edit_advisor(advisor_id):
    try:
        advisor = Advisor.query.get_or_404(advisor_id)
        advisor.name = request.form['name']
        advisor.department = request.form['department']
        advisor.email = request.form['email']
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/admin/advisor/<int:advisor_id>/delete', methods=['POST'])
@admin_required
def admin_delete_advisor(advisor_id):
    try:
        advisor = Advisor.query.get_or_404(advisor_id)
        db.session.delete(advisor)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/log_error', methods=['POST'])
@login_required
def log_error():
    error_data = request.json
    if error_data and 'error' in error_data:
        logging.error(f"Client-side error: {error_data['error']}")
        return jsonify({'message': 'Error logged successfully'}), 200
    else:
        return jsonify({'error': 'Invalid error data'}), 400
