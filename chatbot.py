import spacy
from models import FAQ, Advisor
from app import db

nlp = spacy.load("en_core_web_sm")

def get_intent(text):
    if not text or not text.strip():
        return "empty_input"
    
    doc = nlp(text.lower())
    
    # Simple intent recognition based on keywords
    if any(token.text in ["drop", "withdraw"] for token in doc):
        return "drop_class"
    elif any(token.text in ["register", "enroll", "sign up"] for token in doc):
        return "register_class"
    elif any(token.text in ["advisor", "appointment", "schedule"] for token in doc):
        return "schedule_appointment"
    elif any(token.text in ["calendar", "date", "deadline", "semester", "exam"] for token in doc):
        return "calendar_query"
    else:
        return "general_question"

def extract_date_entities(text):
    doc = nlp(text)
    date_entities = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    return date_entities

def get_response(intent, text):
    if intent == "empty_input":
        return "I'm sorry, but I didn't receive any input. Could you please try again with a question or request?"

    if intent == "drop_class":
        return "To drop a class, you need to follow these steps:\n1. Log in to your student portal\n2. Navigate to 'Course Registration'\n3. Select the class you want to drop\n4. Click on 'Drop Course'\n\nRemember, the deadline for dropping classes is October 31st. Would you like to schedule an appointment with an advisor for more information?"

    elif intent == "register_class":
        return "To register for a class:\n1. Log in to your student portal\n2. Go to 'Course Registration'\n3. Search for the desired course\n4. Click 'Add Course'\n\nMake sure you meet all prerequisites. Do you need help with anything specific?"

    elif intent == "schedule_appointment":
        advisors = Advisor.query.all()
        advisor_list = "\n".join([f"{advisor.name} - {advisor.department}" for advisor in advisors])
        return f"Certainly! Here's a list of available advisors:\n{advisor_list}\n\nTo schedule an appointment, please provide the name of the advisor you'd like to meet with."

    elif intent == "calendar_query":
        date_entities = extract_date_entities(text)
        faqs = FAQ.query.filter(FAQ.category == "Academic Calendar").all()
        
        for faq in faqs:
            if any(entity.lower() in faq.question.lower() for entity in date_entities):
                return faq.answer
        
        # If no specific match is found, return a general calendar response
        return "I couldn't find a specific answer to your calendar query. Here's a summary of important dates:\n\n" + \
               "\n".join([f"{faq.question}: {faq.answer}" for faq in faqs]) + \
               "\n\nFor more detailed information, please check the official academic calendar on our website or contact an advisor."

    else:
        # Search FAQ database for relevant answer
        keywords = [token.lemma_ for token in nlp(text) if not token.is_stop and token.is_alpha]
        if keywords:
            faqs = FAQ.query.filter(FAQ.question.contains(keywords[0])).all()
            if faqs:
                return faqs[0].answer
        
        # Fallback mechanism
        return "I'm sorry, I don't have a specific answer for that question. You can find more information on our official website or in the student handbook. Would you like to schedule an appointment with an advisor for more detailed information?"

def process_message(text):
    if not text or not isinstance(text, str):
        return "I'm sorry, but I couldn't process your input. Please try again with a valid text message."
    
    intent = get_intent(text)
    response = get_response(intent, text)
    return response
