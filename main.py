from playsound import playsound
import speech_recognition as sr
from gtts import gTTS
import requests
from bs4 import BeautifulSoup
import time
import os

def speak(audio):
    try:
        print(str(audio))
        tts = gTTS(text=audio, lang='tl')
        audio_file = 'temp.mp3'
        tts.save(audio_file)
        playsound(audio_file)
        os.remove(audio_file)
    except Exception as e:
        print(f"Error sa speak function: {e}")

def greet_user():
    greetings = [
        "Hi, ako si Jocelyn! Paano kita matutulungan ngayon?",
        "Hello! Sana ay maganda ang araw mo!",
        "Kumusta! Ano ang maitutulong ko sa iyo?"
    ]
    return greetings

def leave_message():
    messages = [
        "Mukhang walang sumasagot. Nandito lang ako kung kailangan mo ako. Magandang araw!",
        "Walang sagot na natukoy. Pa alam!",
    ]
    return messages

def get_weather():
    search_query = "Iloilo City weather"
    google_search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(google_search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find weather information
        weather_info = soup.find("div", class_="BNeawe").text
        temperature = soup.find("div", class_="BNeawe iBp4i AP7Wnd").text
        weather_report = f"Ang kasalukuyang panahon sa Iloilo City ay {weather_info} at ang temperatura ay {temperature}."

    except Exception as e:
        weather_report = "Pasensya, hindi ko makuha ang datos ng panahon sa ngayon."
    
    return weather_report

# Greet the user when the script starts
try:
    greeting_message = greet_user()
    speak(greeting_message[0])  # You can choose which greeting to use
except Exception as e:
    print(f"Error sa paunang pagbati: {e}")

leave_message_spoken = False  # Flag to track if leave message has been spoken
inactivity_timeout = 30  # Time in seconds to wait before speaking leave message
last_interaction_time = time.time()

while True:
    try:
        with sr.Microphone() as source:
            print('(oo)')
            audio = sr.Recognizer().listen(source, timeout=5)  # Added timeout to avoid long waits
            print("(..)")
            query = sr.Recognizer().recognize_google(audio, language='tl')
            word = str(query).lower()
            print(word)

            if word == '' or word == ' ':
                continue

            # Update last interaction time
            last_interaction_time = time.time()

            # Respond to specific keywords
            if "hello" in word or "hi" in word:
                response_message = "Hello! Paano kita matutulungan?"
            elif "weather" in word:
                response_message = get_weather()
            else:
                response_message = "Pasensya, hindi ko naintindihan ang iyong sinasabi."

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
            response_message = leave_message()[1]  # You can choose which leave message to use
            speak(response_message)
            leave_message_spoken = True  # Set flag to avoid repeating the leave message

    # Check if inactivity timeout has been reached
    current_time = time.time()
    if current_time - last_interaction_time > inactivity_timeout:
        if not leave_message_spoken:
            response_message = leave_message()[0]  # You can choose which leave message to use
            speak(response_message)
            leave_message_spoken = True  # Set flag to avoid repeating the leave message
