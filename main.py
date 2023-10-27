from playsound import playsound
import speech_recognition as sr
import pyttsx3
import openai
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine = pyttsx3.init()
engine.setProperty('rate', 160)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
def speak(audio):
    print(str(audio))
    engine.say(audio)
    engine.runAndWait()
openai.api_key = "your api"
speak('hello niel gwapo, everything good bro? how can I help you today? I gotchu homie')
while True:
    try:
        with sr.Microphone() as source:
            print('(oo)')
            audio = sr.Recognizer().listen(source)
            print("(..)")
            qwery = sr.Recognizer().recognize_google(audio, language='en-in')
            word = str(qwery).lower()
            print(word)   
            if word == '' or word == ' ':
                continue
            response = openai.Completion.create(model="gpt-3.5-turbo-0613", prompt=word, temperature=0, max_tokens=100)
            res = response['choices'][0]['text']
            speak(res)
    except Exception as e:
        print(e)