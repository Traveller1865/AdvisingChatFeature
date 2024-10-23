import spacy
import re
from models import FAQ, Advisor
from app import db
import logging

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logging.error("Spacy model not found. Please run: python -m spacy download en_core_web_sm")
    nlp = None

def preprocess_text(text):
    if not text or not isinstance(text, str):
        return ""
    # Clean and normalize text
    text = text.lower().strip()
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^a-z0-9\s.,?!]', '', text)
    return text

def extract_entities(text):
    if not nlp:
        return {}
    
    doc = nlp(text)
    entities = {
        'dates': [],
        'people': [],
        'subjects': []
    }
    
    # Extract named entities
    for ent in doc.ents:
        if ent.label_ == 'DATE':
            entities['dates'].append(ent.text)
        elif ent.label_ == 'PERSON':
            entities['people'].append(ent.text)
        elif ent.label_ in ['ORG', 'PRODUCT']:
            entities['subjects'].append(ent.text)
    
    return entities

def get_intent(text):
    if not text or not isinstance(text, str):
        return "empty_input"
    
    text = preprocess_text(text)
    if not nlp:
        # Fallback to keyword matching if spaCy is not available
        return get_intent_by_keywords(text)
    
    doc = nlp(text)
    
    # Intent classification using spaCy's linguistic features
    if any(token.dep_ == 'ROOT' and token.lemma_ in ['drop', 'withdraw'] for token in doc):
        return "drop_class"
    elif any(token.dep_ == 'ROOT' and token.lemma_ in ['register', 'enroll', 'sign'] for token in doc):
        return "register_class"
    elif any(token.lemma_ in ['schedule', 'book', 'meet', 'appointment'] for token in doc):
        return "schedule_appointment"
    elif any(token.lemma_ in ['deadline', 'when', 'date', 'time'] for token in doc):
        return "calendar_query"
    elif any(token.text == 'how' and any(t.text == 'many' for t in token.children) for token in doc):
        return "count_query"
    
    # Check for question types
    question_words = ['what', 'how', 'why', 'when', 'where', 'who']
    if any(token.lemma_ in question_words for token in doc):
        return "information_query"
    
    return "general_question"

def get_intent_by_keywords(text):
    # Fallback keyword-based intent recognition
    if any(word in text for word in ["drop", "withdraw"]):
        return "drop_class"
    elif any(word in text for word in ["register", "enroll", "sign up"]):
        return "register_class"
    elif any(word in text for word in ["advisor", "appointment", "schedule"]):
        return "schedule_appointment"
    elif any(word in text for word in ["calendar", "date", "deadline", "semester", "exam"]):
        return "calendar_query"
    elif ("count" in text or "how many" in text) and "advisor" in text:
        return "count_advisors"
    return "general_question"

def find_best_faq_match(text, intent):
    if not nlp:
        return None
        
    # Convert user query to spaCy doc
    user_doc = nlp(preprocess_text(text))
    
    # Get FAQs from database
    faqs = FAQ.query.all()
    best_match = None
    highest_similarity = 0.4  # Threshold for similarity
    
    for faq in faqs:
        # Compare question similarity using spaCy
        faq_doc = nlp(preprocess_text(faq.question))
        similarity = user_doc.similarity(faq_doc)
        
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = faq
            
    return best_match

def get_response(intent, text):
    if intent == "empty_input":
        return "I'm sorry, but I didn't receive any input. Could you please try again with a question or request?"

    # Extract entities from text
    entities = extract_entities(text)
    
    # Handle different intents with entity awareness
    if intent == "drop_class":
        response = "To drop a class, you need to follow these steps:\n"
        response += "1. Log in to your student portal\n"
        response += "2. Navigate to 'Course Registration'\n"
        response += "3. Select the class you want to drop\n"
        response += "4. Click on 'Drop Course'\n\n"
        
        if entities['dates']:
            response += f"Note: The mentioned date {entities['dates'][0]} might be important for the drop deadline. "
        else:
            response += "Remember, the deadline for dropping classes is October 31st. "
        
        return response + "Would you like to schedule an appointment with an advisor for more information?"

    elif intent == "register_class":
        subjects = entities['subjects']
        response = "To register for a class:\n"
        response += "1. Log in to your student portal\n"
        response += "2. Go to 'Course Registration'\n"
        response += "3. Search for the desired course\n"
        response += "4. Click 'Add Course'\n\n"
        
        if subjects:
            response += f"I notice you're interested in {', '.join(subjects)}. "
        
        return response + "Make sure you meet all prerequisites. Do you need help with anything specific?"

    elif intent == "schedule_appointment":
        advisors = Advisor.query.all()
        if entities['people']:
            # Look for specific advisor mentioned
            advisor_name = entities['people'][0]
            advisor = Advisor.query.filter(Advisor.name.ilike(f"%{advisor_name}%")).first()
            if advisor:
                return f"I can help you schedule an appointment with {advisor.name} from the {advisor.department} department. Please confirm if you'd like to proceed with scheduling."
        
        if advisors:
            advisor_list = "\n".join([f"• {advisor.name} - {advisor.department}" for advisor in advisors])
            return f"Here are our available advisors:\n{advisor_list}\n\nTo schedule an appointment, please let me know which advisor you'd like to meet with."
        return "I apologize, but there are currently no advisors available in the system. Please check back later or contact the advising office directly."

    elif intent == "calendar_query":
        if entities['dates']:
            # Search for FAQs containing the mentioned dates
            date_str = entities['dates'][0]
            faqs = FAQ.query.filter(FAQ.category == "Academic Calendar").all()
            for faq in faqs:
                if date_str in faq.question or date_str in faq.answer:
                    return faq.answer
        
        # Default calendar response
        faqs = FAQ.query.filter(FAQ.category == "Academic Calendar").all()
        return "Here are the important academic dates:\n\n" + \
               "\n".join([f"• {faq.question}: {faq.answer}" for faq in faqs])

    # Try to find matching FAQ for general questions
    faq_match = find_best_faq_match(text, intent)
    if faq_match:
        return faq_match.answer
    
    return "I'm sorry, I don't have a specific answer for that question. You can find more information on our official website or in the student handbook. Would you like to schedule an appointment with an advisor for more detailed information?"

def process_message(text):
    if not text or not isinstance(text, str):
        return "I'm sorry, but I couldn't process your input. Please try again with a valid text message."
    
    # Preprocess the text
    processed_text = preprocess_text(text)
    
    # Get intent
    intent = get_intent(processed_text)
    
    # Generate response
    response = get_response(intent, processed_text)
    
    return response
