import spacy
import re
from models import FAQ, Advisor
from app import db
import logging

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logging.error("Spacy model not found. Please install it using python -m spacy download en_core_web_sm")
    nlp = None

def preprocess_text(text):
    if not text or not isinstance(text, str):
        return ""
    # Enhanced text preprocessing
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s.,?!]', '', text)
    return text

def extract_entities(text):
    if not nlp:
        return {}
    
    doc = nlp(text)
    entities = {
        'dates': [],
        'people': [],
        'subjects': [],
        'courses': [],
        'locations': []
    }
    
    # Enhanced entity extraction
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            entities['dates'].append(ent.text)
        elif ent.label_ == 'PERSON':
            entities['people'].append(ent.text)
        elif ent.label_ in ['ORG', 'PRODUCT']:
            entities['subjects'].append(ent.text)
        elif ent.label_ == 'GPE':
            entities['locations'].append(ent.text)
    
    # Extract course numbers using regex
    course_pattern = r'\b[A-Z]{2,4}\s*\d{3}\b'
    courses = re.findall(course_pattern, text.upper())
    entities['courses'].extend(courses)
    
    return entities

def get_intent(text):
    if not text or not isinstance(text, str):
        return "empty_input"
    
    text = preprocess_text(text)
    if not nlp:
        return get_intent_by_keywords(text)
    
    doc = nlp(text)
    
    # Enhanced intent classification
    intents = {
        'drop_class': ['drop', 'withdraw', 'remove', 'quit'],
        'register_class': ['register', 'enroll', 'sign up', 'add class'],
        'schedule_appointment': ['schedule', 'book', 'meet', 'appointment', 'advisor'],
        'deadline_query': ['deadline', 'due date', 'when', 'last day'],
        'prerequisite_query': ['prerequisite', 'require', 'needed', 'eligible'],
        'grade_query': ['grade', 'gpa', 'score', 'pass'],
        'financial_aid': ['financial aid', 'scholarship', 'grant', 'loan'],
        'transfer_credit': ['transfer', 'credit', 'equivalent']
    }
    
    # Check for specific action verbs
    main_verb = None
    for token in doc:
        if token.dep_ == 'ROOT' and token.pos_ == 'VERB':
            main_verb = token.lemma_
    
    # Match intents based on keywords and context
    for intent, keywords in intents.items():
        if main_verb and any(keyword in main_verb for keyword in keywords):
            return intent
        if any(keyword in text for keyword in keywords):
            return intent
    
    # Check for question types
    if any(token.tag_ == 'WDT' or token.tag_ == 'WP' or token.tag_ == 'WRB' for token in doc):
        return "information_query"
    
    return "general_question"

def get_intent_by_keywords(text):
    # Enhanced keyword-based intent detection
    intent_patterns = {
        'drop_class': [r'\b(drop|withdraw|quit)\b.*\b(class|course)\b'],
        'register_class': [r'\b(register|enroll|sign)\b.*\b(class|course)\b'],
        'schedule_appointment': [r'\b(schedule|book|meet)\b.*\b(advisor|appointment)\b'],
        'deadline_query': [r'\b(when|deadline|due date)\b'],
        'prerequisite_query': [r'\b(prerequisite|require|need)\b'],
        'grade_query': [r'\b(grade|gpa|score)\b'],
        'financial_aid': [r'\b(financial aid|scholarship|grant|loan)\b'],
        'transfer_credit': [r'\b(transfer|credit)\b']
    }
    
    for intent, patterns in intent_patterns.items():
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
            return intent
    
    return "general_question"

def get_response(intent, text):
    entities = extract_entities(text)
    
    responses = {
        'empty_input': "I'm sorry, but I didn't receive any input. Could you please try again with a question or request?",
        'drop_class': generate_drop_class_response(entities),
        'register_class': generate_register_class_response(entities),
        'schedule_appointment': generate_appointment_response(entities),
        'deadline_query': generate_deadline_response(entities),
        'prerequisite_query': generate_prerequisite_response(entities),
        'grade_query': generate_grade_response(entities),
        'financial_aid': generate_financial_aid_response(entities),
        'transfer_credit': generate_transfer_credit_response(entities)
    }
    
    response = responses.get(intent)
    if response:
        return response
    
    # Try to find matching FAQ for general questions
    faq_match = find_best_faq_match(text)
    if faq_match:
        return faq_match.answer
    
    return "I'm sorry, I don't have a specific answer for that question. You can find more information on our official website or in the student handbook. Would you like to schedule an appointment with an advisor for more detailed information?"

def process_message(text):
    if not text or not isinstance(text, str):
        return "I'm sorry, but I couldn't process your input. Please try again with a valid text message."
    
    processed_text = preprocess_text(text)
    intent = get_intent(processed_text)
    return get_response(intent, processed_text)

# Helper functions for generating specific responses
def generate_drop_class_response(entities):
    response = "To drop a class, follow these steps:\n"
    response += "1. Log in to your student portal\n"
    response += "2. Navigate to 'Course Registration'\n"
    response += "3. Select the class you want to drop\n"
    response += "4. Click on 'Drop Course'\n\n"
    
    if entities['courses']:
        response += f"I see you're interested in dropping {', '.join(entities['courses'])}. "
    if entities['dates']:
        response += f"Note: The mentioned date {entities['dates'][0]} might be important for the drop deadline. "
    
    return response + "Would you like to schedule an appointment with an advisor for more information?"

def generate_register_class_response(entities):
    response = "To register for a class:\n"
    response += "1. Log in to your student portal\n"
    response += "2. Go to 'Course Registration'\n"
    response += "3. Search for the desired course\n"
    response += "4. Click 'Add Course'\n\n"
    
    if entities['courses']:
        response += f"I see you're interested in {', '.join(entities['courses'])}. "
    if entities['subjects']:
        response += f"The following subjects were mentioned: {', '.join(entities['subjects'])}. "
    
    return response + "Make sure you meet all prerequisites. Do you need help with anything specific?"

def generate_appointment_response(entities):
    advisors = Advisor.query.all()
    if entities['people']:
        advisor_name = entities['people'][0]
        advisor = Advisor.query.filter(Advisor.name.ilike(f"%{advisor_name}%")).first()
        if advisor:
            return f"I can help you schedule an appointment with {advisor.name} from the {advisor.department} department. Please confirm if you'd like to proceed with scheduling."
    
    if advisors:
        advisor_list = "\n".join([f"• {advisor.name} - {advisor.department}" for advisor in advisors])
        return f"Here are our available advisors:\n{advisor_list}\n\nTo schedule an appointment, please let me know which advisor you'd like to meet with."
    
    return "I apologize, but there are currently no advisors available in the system. Please check back later or contact the advising office directly."

def generate_deadline_response(entities):
    if entities['dates']:
        date_str = entities['dates'][0]
        faqs = FAQ.query.filter(FAQ.category == "Academic Calendar").all()
        for faq in faqs:
            if date_str in faq.question or date_str in faq.answer:
                return faq.answer
    
    faqs = FAQ.query.filter(FAQ.category == "Academic Calendar").all()
    return "Here are the important academic dates:\n\n" + \
           "\n".join([f"• {faq.question}: {faq.answer}" for faq in faqs])

def generate_prerequisite_response(entities):
    response = "To check prerequisites for a course:\n"
    response += "1. Visit the course catalog\n"
    response += "2. Search for your desired course\n"
    response += "3. Review the prerequisites section\n\n"
    
    if entities['courses']:
        response += f"For specific prerequisites for {', '.join(entities['courses'])}, "
        response += "please consult the course catalog or speak with an advisor."
    
    return response

def generate_grade_response(entities):
    return "For grade-related queries, please check your student portal or schedule an appointment with your academic advisor for a detailed discussion about your academic progress."

def generate_financial_aid_response(entities):
    return "For financial aid information, please visit the Financial Aid office or check their website. You can also schedule an appointment with a financial aid advisor for personalized assistance."

def generate_transfer_credit_response(entities):
    response = "For transfer credits:\n"
    response += "1. Submit your official transcripts\n"
    response += "2. Complete a transfer credit evaluation form\n"
    response += "3. Meet with an advisor to review your credits\n\n"
    
    if entities['courses']:
        response += f"For specific information about transferring {', '.join(entities['courses'])}, "
        response += "please schedule an appointment with an advisor."
    
    return response

def find_best_faq_match(text):
    if not nlp:
        return None
    
    user_doc = nlp(preprocess_text(text))
    faqs = FAQ.query.all()
    best_match = None
    highest_similarity = 0.4  # Threshold for similarity
    
    for faq in faqs:
        faq_doc = nlp(preprocess_text(faq.question))
        similarity = user_doc.similarity(faq_doc)
        
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = faq
    
    return best_match
