# actions/actions.py

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionScheduleAppointment(Action):
    def name(self) -> Text:
        return "action_schedule_appointment"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        advisor_type = tracker.get_slot('advisor_type')
        date = tracker.get_slot('date')
        time = tracker.get_slot('time')
        meeting_type = tracker.get_slot('meeting_type')

        confirmation_message = (
            f"Your {meeting_type} meeting with a {advisor_type} has been scheduled for "
            f"{date} at {time}. You will receive a confirmation email shortly."
        )
        dispatcher.utter_message(text=confirmation_message)

        return [
            SlotSet("advisor_type", None),
            SlotSet("date", None),
            SlotSet("time", None),
            SlotSet("meeting_type", None)
        ]


class ActionProvideInformation(Action):
    def name(self) -> Text:
        return "action_provide_information"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        topic = tracker.get_slot('topic')

        # Here you can integrate with the university catalog or database
        # For demonstration, we'll use a placeholder response

        information_database = {
            "SELU": "SELU stands for Student Engagement and Learning Unit, which provides various resources to support your academic journey.",
            "School of Engineering": "The School of Engineering offers programs in Computer Science, Mechanical Engineering, and Civil Engineering.",
            "Library Services": "Library Services offers access to books, journals, and online resources to support your studies.",
            "Academic Calendar": "The academic year starts on September 1st and ends on June 30th. Registration deadlines are October 31st and April 30th.",
            "Course Catalog": "The Course Catalog provides detailed descriptions of all courses, including prerequisites and credit information.",
            # Add more topics as needed
        }

        response = information_database.get(topic, "I'm sorry, I don't have information on that topic. Please try asking about something else.")

        dispatcher.utter_message(text=response)

        return []


class ActionHandleFeedback(Action):
    def name(self) -> Text:
        return "action_handle_feedback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        feedback = tracker.latest_message.get('text')

        dispatcher.utter_message(text="Thank you for your feedback! We appreciate your input and will work on improving our services.")

        # Here, you might want to save the feedback to a database or send it via email

        return []


class ActionProvideResourceInfo(Action):
    def name(self) -> Text:
        return "action_provide_resource_info"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        resource = tracker.get_slot('resource') or tracker.get_slot('service') or tracker.get_slot('location')

        # Placeholder for resource information
        resource_database = {
            "tutoring services": "Tutoring services are available at the Academic Success Center located in Building A, Room 101.",
            "writing center": "The Writing Center offers assistance with writing assignments and is located in Building B, Room 202.",
            "mental health services": "Counseling and mental health services are available at the Wellness Center.",
            # Add more resources as needed
        }

        response = resource_database.get(resource.lower(), "I'm sorry, I don't have information on that resource. Please specify the resource you're interested in.")

        dispatcher.utter_message(text=response)

        return []
