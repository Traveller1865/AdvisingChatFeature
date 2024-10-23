import re
from models import FAQ, Advisor
from app import db

def get_intent(text):
    if not text or not isinstance(text, str):
        return "empty_input"
    
    text = text.lower()
    # Simple keyword-based intent recognition
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
    else:
        return "general_question"

def get_response(intent, text):
    if intent == "empty_input":
        return "I'm sorry, but I didn't receive any input. Could you please try again with a question or request?"

    if intent == "drop_class":
        return "To drop a class, you need to follow these steps:\n1. Log in to your student portal\n2. Navigate to 'Course Registration'\n3. Select the class you want to drop\n4. Click on 'Drop Course'\n\nRemember, the deadline for dropping classes is October 31st. Would you like to schedule an appointment with an advisor for more information?"

    elif intent == "register_class":
        return "To register for a class:\n1. Log in to your student portal\n2. Go to 'Course Registration'\n3. Search for the desired course\n4. Click 'Add Course'\n\nMake sure you meet all prerequisites. Do you need help with anything specific?"

    elif intent == "schedule_appointment":
        advisors = Advisor.query.all()
        if advisors:
            advisor_list = "\n".join([f"{advisor.name} - {advisor.department}" for advisor in advisors])
            return f"Certainly! Here's a list of available advisors:\n{advisor_list}\n\nTo schedule an appointment, please provide the name of the advisor you'd like to meet with."
        else:
            return "I apologize, but there are currently no advisors available in the system. Please check back later or contact the advising office directly."

    elif intent == "calendar_query":
        # Simple date extraction using regex for common formats
        date_pattern = r'\b\d{1,2}/\d{1,2}/\d{2,4}\b|\b\d{4}-\d{1,2}-\d{1,2}\b'
        dates = re.findall(date_pattern, text)
        
        faqs = FAQ.query.filter(FAQ.category == "Academic Calendar").all()
        
        if dates and faqs:
            relevant_faqs = [faq for faq in faqs if any(date in faq.question or date in faq.answer for date in dates)]
            if relevant_faqs:
                return relevant_faqs[0].answer
        
        # If no specific match is found, return a general calendar response
        return "Here are the important academic dates:\n\n" + \
               "\n".join([f"• {faq.question}: {faq.answer}" for faq in faqs])

    elif intent == "count_advisors":
        advisor_count = Advisor.query.count()
        if advisor_count == 0:
            return "I'm sorry, but there are currently no advisors registered in our system."
        elif advisor_count == 1:
            return "There is currently 1 advisor available in our system."
        else:
            return f"There are currently {advisor_count} advisors available in our system."

    else:
        # Search FAQ database for relevant answer using simple keyword matching
        words = set(text.lower().split())
        faqs = FAQ.query.all()
        
        for faq in faqs:
            question_words = set(faq.question.lower().split())
            if len(words & question_words) >= 2:  # If at least 2 words match
                return faq.answer
        
        return "I'm sorry, I don't have a specific answer for that question. You can find more information on our official website or in the student handbook. Would you like to schedule an appointment with an advisor for more detailed information?"

def process_message(text):
    if not text or not isinstance(text, str):
        return "I'm sorry, but I couldn't process your input. Please try again with a valid text message."
    
    # Simple text cleanup
    text = text.strip()
    
    intent = get_intent(text)
    response = get_response(intent, text)
    return response
