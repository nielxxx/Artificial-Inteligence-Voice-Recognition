from playsound import playsound
import speech_recognition as sr
import pyttsx3



# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    print(str(audio))
    engine.say(audio)
    engine.runAndWait()

def greet_user():
    greetings = [
        "Hi there! How can I help you today?",
        "Hello! I hope you're having a great day!",
        "Greetings! What can I do for you?"
    ]
    return greetings

def leave_message():
    messages = [
        "It seems like no one is answering. Have a great day!",
        "No response detected. Goodbye!",
        "I'll be here if you need anything. Have a good one!"
    ]
    return messages

# Greet the user when the script starts
greeting_message = greet_user()
speak(greeting_message[0])  # You can choose which greeting to use

leave_message_spoken = False  # Flag to track if leave message has been spoken

while True:
    try:
        with sr.Microphone() as source:
            print('(oo)')
            audio = sr.Recognizer().listen(source, timeout=5)  # Added timeout to avoid long waits
            print("(..)")
            query = sr.Recognizer().recognize_google(audio, language='en-in')
            word = str(query).lower()
            print(word)

            if word == '' or word == ' ':
                continue

            # Simple condition to respond based on the query
            if "hello" in word or "hi" in word:
                response_message = "Hello! How can I assist you?"
            else:
                response_message = "Sorry, I didn't understand that."

            speak(response_message)
            leave_message_spoken = False  # Reset leave message flag on successful interaction
            
    except sr.UnknownValueError:
        # Handle cases where speech is not recognized
        if not leave_message_spoken:
            response_message = leave_message()[0]  # You can choose which leave message to use
            speak(response_message)
            leave_message_spoken = True  # Set flag to avoid repeating the leave message
    except sr.RequestError as e:
        # Handle cases where the request fails
        print(f"Request error: {e}")
        if not leave_message_spoken:
            response_message = leave_message()[1]  # You can choose which leave message to use
            speak(response_message)
            leave_message_spoken = True  # Set flag to avoid repeating the leave message
    except Exception as e:
        print(e)
        if not leave_message_spoken:
            response_message = leave_message()[2]  # You can choose which leave message to use
            speak(response_message)
            leave_message_spoken = True  # Set flag to avoid repeating the leave message
