

from speech_handler import SpeechAssistant
from T5_inf import T5Inference
from check import CheckData
import time
from messenger import RPIClient
#from eth import Comms
import csv


PROMPT = """Can you read the text and identify the task, the destination room (if mentioned), and the person's name (if mentioned)? 
                If the destination room or the person's name is not mentioned, please specify 'none'. And, if the text says to avoid the first 
                mentioned name and room number and provides a second name or room number or both, only focus on the second name and room number."  
                """

INTRO = """Hi, My name is Alpha. I am a robotic guide dog designed to help you navigate the IAS institute.
            If you need my help, say 'Hi Alpha'. I will be ready to assist you. 
            Listen for a beep sound before speaking.
            It lets me know when to listen carefully. """



def intro(speech_assistant):
    speech_assistant.speak_text(INTRO)



def extract_nav_info(name):
    # Load CSV data into a list of dictionaries (name and room pairs)
    csv_file = "nav_info.csv"
    data = []
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({"name_csv": row["name"], "nav_info": row["nav_info"]})
    #print(data)
    for entry in data:
        if entry["name_csv"] == name:
            return entry["nav_info"]


    

def handle_navigation(name, room):
    """
    Handles navigation based on the task, person_name, and destination_room.
    If task is 'navigation', prompt the user for confirmation. Also, a 
    """
    nav_info = extract_nav_info(name=name)
    print(f"Send nav info to robot for navigation {nav_info}")

    # send the destination info to navigation stack in robot
    agent = RPIClient("192.168.2.1", port=65432)
    agent.connect()
    print("sending msg to navigation handler")
    agent.send_message(nav_info)
    received_msg = agent.receive_message()
    print(f"Message received from navigation: {received_msg}")
    if received_msg == "navigation_completed":
        return True
    agent.close()
    #agent = Communicator(nav_info)
    #agent.send_message()
    #check_navigation_status()
    #print(f"navigating to {name} in room {room}")
    #time.sleep(30)
    #return True
    

def check_navigation_status():
    # listen if navigation is completed, if yes return True to handle_navigation() function
    # navigation_status completed when the destination room is reached, then send the robot back to home position and notify
    # as home

    pass


def listen_for_keyword(speech_assistant):
    """Listen for the specific keyword to initiate assistance."""
    while True:
        if speech_assistant.listen_for_keyword():  # Assuming this returns True when the keyword is detected
            return True


def listen_for_speech(speech_assistant):
    """Listen for user speech and return the recognized text."""
    recognized_text = speech_assistant.listen_for_speech()
    return recognized_text


def ask_for_navigation_confirmation(speech_assistant, verified_name, verified_room):
    """Ask the user for navigation confirmation."""
    speech_assistant.speak_text(f"Do you want to go to {verified_name}'s room in room number {verified_room}? Please say 'yes' or 'no'")
    print(f"Do you want to go to {verified_name}'s room in room number {verified_room}? Please say 'yes' or 'no'")
    time.sleep(2)

    while True:
        confirmation_response = speech_assistant.listen_for_speech()
        
        if "yes" in confirmation_response.lower():
            return True  # User wants to proceed
        elif "no" in confirmation_response.lower():
            return False  # User does not want to proceed
        else:
            speech_assistant.speak_text("I did not understand that. Please say 'yes' or 'no'")



# Main function to handle the flow of events

if __name__ == "__main__":

    speech_assistant = SpeechAssistant(listen_timeout=30, speech_timeout=30, speech_duration=10)
    intro(speech_assistant)
    time.sleep(5)
    inference = T5Inference()

    while True:
        listen_for_keyword(speech_assistant)  # Wait for the keyword
        speech_assistant.speak_text("How may I help you?")

        # Now, directly listen for speech after the prompt
        recognized_text = listen_for_speech(speech_assistant)  # Listen for user speech

        if recognized_text:
            result = inference.generate_answer(recognized_text, PROMPT)

            # If the task is "navigation"
            if result["task"] == "navigation":
                name_to_check = result["name"]
                room_to_check = result["room"]
                checker = CheckData(name_to_check=name_to_check, room_to_check=room_to_check)
                verified_data = checker.process_data()
                verified_name = verified_data[0]
                verified_room = verified_data[1]

                # Ask for navigation confirmation
                if ask_for_navigation_confirmation(speech_assistant, verified_name, verified_room):
                    
                    # Handle navigation and get the result
                    speech_assistant.speak_text(f"Navigating to {verified_name} in room {verified_room}. Please follow me")
                    navigation_status = handle_navigation(verified_name, verified_room)

                    if navigation_status:
                        speech_assistant.speak_text("Navigation completed successfully. Thank you for visiting")
                        time.sleep(20)
                        
                        #home_notification
                        #agent = Comms()
                        #received_msg = agent.receive_from()
                            #speech_assistant.speak_text("Thank you for visiting.")  
                        time.sleep(3)      
                        intro(speech_assistant)

                    else:
                        speech_assistant.speak_text("Navigation failed. Please try again")
                        time.sleep(2)
                        speech_assistant.speak_text("Say Hi Alpha if you need my help.")
                        speech_assistant.play_beep()
                else:
                    speech_assistant.speak_text("Say Hi Alpha if you need my help.")
                    speech_assistant.play_beep()
                # If the user said "no", the loop naturally continues here to ask for more speech



                    