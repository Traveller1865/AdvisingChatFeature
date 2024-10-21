import spacy
from models import FAQ, Advisor
from app import db

nlp = spacy.load("en_core_web_sm")

def get_intent(text):
    doc = nlp(text.lower())
    
    # Simple intent recognition based on keywords
    if any(token.text in ["drop", "withdraw"] for token in doc):
        return "drop_class"
    elif any(token.text in ["register", "enroll", "sign up"] for token in doc):
        return "register_class"
    elif any(token.text in ["advisor", "appointment", "schedule"] for token in doc):
        return "schedule_appointment"
    else:
        return "general_question"

def get_response(intent, text):
    if intent == "drop_class":
        return "To drop a class, you need to follow these steps:\n1. Log in to your student portal\n2. Navigate to 'Course Registration'\n3. Select the class you want to drop\n4. Click on 'Drop Course'\n\nRemember, the deadline for dropping classes is October 31st. Would you like to schedule an appointment with an advisor for more information?"

    elif intent == "register_class":
        return "To register for a class:\n1. Log in to your student portal\n2. Go to 'Course Registration'\n3. Search for the desired course\n4. Click 'Add Course'\n\nMake sure you meet all prerequisites. Do you need help with anything specific?"

    elif intent == "schedule_appointment":
        advisors = Advisor.query.all()
        advisor_list = "\n".join([f"{advisor.name} - {advisor.department}" for advisor in advisors])
        return f"Certainly! Here's a list of available advisors:\n{advisor_list}\n\nTo schedule an appointment, please provide the name of the advisor you'd like to meet with."

    else:
        # Search FAQ database for relevant answer
        keywords = [token.lemma_ for token in nlp(text) if not token.is_stop and token.is_alpha]
        faqs = FAQ.query.filter(FAQ.question.contains(keywords[0]) if keywords else "").all()
        
        if faqs:
            return faqs[0].answer
        else:
            return "I'm sorry, I don't have a specific answer for that question. Would you like to schedule an appointment with an advisor for more detailed information?"

def process_message(text):
    intent = get_intent(text)
    response = get_response(intent, text)
    return response
