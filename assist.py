import pyttsx3
import speech_recognition as sr
import pyaudio
import datetime
import webbrowser
import pyjokes
import randfacts
import os
import psutil
import wikipedia
import pyautogui
import requests
import json
import weathercom
from wikisel import *
from selyt import *

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id) '''To get the list of voices present in your system '''
engine.setProperty('voice',voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#speak("Hello everyone")

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio,language="en-in")
            print(f"User said: {query}\n")

        except Exception as e:
            print("I am sorry , Please repeat it")
            return "None"
        return query

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning")

    elif hour>=12 and hour<18:
        speak("Good Afternoon")

    else:
        speak("Good evening")

def weatherreport(city):
    weatherdetails = weathercom.getCityWeatherDetails(city)
    humidity = json.loads(weatherdetails)["vt1observation"]["humidity"]
    temp = json.loads(weatherdetails)["vt1observation"]["temperature"]
    pharse = json.loads(weatherdetails)["vt1observation"]["phrase"]
    return humidity,temp,pharse

if __name__ == '__main__':
    wishMe()
    speak("I am your Personal Assistant , How are you sir?")
    while True:
        text = takecommand().lower()

        if "what" in text and "about" in text and "you" in text:
            speak("I am good sir, What can i do for you?")

        elif "time" in text:
            curTime = datetime.datetime.now().strftime("%I :%M :%S %p")
            # %H -hour
            # %M - minutes
            # %S - seconds
            # %I - hour (12hr)
            # %p - am or pm
            print(f"The time is {curTime}")
            speak(f"The time is {curTime}")

        elif "date" in text:
            curDate = datetime.datetime.now().strftime("%d:%B:%Y")
            curDay = datetime.datetime.now().strftime("%A")
            # %d - date
            # %B - month
            # %Y - year
            # %A - day
            print(f"Today's date is {curDate} and it is {curDay}")
            speak(f"Today's date is {curDate} and it is {curDay}")

        elif "open" and "google" in text:
            speak("Opening Google in your Browser")
            webbrowser.open(url="https://google.com")

        elif "open" and "youtube" in text:
            speak("Opening Youtube in your Browser")
            webbrowser.open(url="https://youtube.com")

        elif "joke" in text:
            J = pyjokes.get_joke('en','neutral')
            print(J)
            speak(J)

        elif "fact" in text:
            F = randfacts.getFact()
            print(F)
            speak(F)

        elif "open" in text and "code" in text:
            speak("Opening Visual Studio Code")
            codePath = "C:\\Users\\pvvha\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe" #Path of the application
            os.startfile(codePath)

        elif "cpu stats" in text:
            usage = str(psutil.cpu_percent())
            speak('CPU is at ' + usage)

            battery = psutil.sensors_battery()
            speak("Battery is at")
            speak(battery.percent)

        elif "according to wikipedia" in text:
            speak("Searching in wikipedia...")
            word = text.replace("wikipedia","")
            results = wikipedia.summary(word,sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)

        elif "take" in text and "screenshot" in text:
            img = pyautogui.screenshot()
            speak("Done sir , saving it.")
            img.save('C:\\Users\\pvvha\\Desktop\\session\\perassist\\img.png')

        elif "take notes" in text:
            speak("What should i write sir?")
            notes = takecommand()
            file = open('notes.txt','w')
            speak("Should i include date and time ?")
            ans = takecommand()
            if "yes" or "sure" in ans:
                curTime = datetime.datetime.now().strftime("%I :%M :%S %p")
                curDate = datetime.datetime.now().strftime("%d:%B:%Y")
                file.write(curTime)
                file.write(curDate)
                file.write(':-')
                file.write(notes)
                speak("Done taking notes sir")

            else:
                file.write(notes)
                speak("Done taking notes sir")

        elif "show notes" in text:
            speak("Opening notes")
            file = open('notes.txt','r')
            print(file.read())
            speak(file.read())

        elif "news" in text:
            api_address = "https://newsapi.org/v2/top-headlines?country=in&apiKey=put your newsapi key here"

            response = requests.get(api_address)
            news_json = json.loads(response.text)

            count = 3 #no of news articles
            print("Here are today's Top headlines")
            speak("Here are today's Top headlines")
            for news in news_json['articles']:
                if count >0:
                    T = str(news['title'])
                    print(T)
                    speak(T)
                    count -= 1

        elif "weather" in text:
            print("Sure sir, please name me the city")
            speak("Sure sir, please name me the city")
            city = takecommand()
            humidity , temp , phrase = weatherreport(city)
            print("Currently in "+ city + "the temperature is "+str(temp)+" degree celcius ,with humidity of "
                  + str(humidity) + "percent and sky is " + phrase)
            speak("Today's weather report : Currently in "+ city + "the temperature is "+str(temp)+" degree celcius ,with humidity of "
                  + str(humidity) + "percent and sky is " + phrase)

        elif "information" in text:
            speak("Please name the topic sir")
            topic = takecommand()
            print("Searching {} in wikipedia".format(topic))
            speak("Searching {} in wikipedia".format(topic))
            assit = info()
            assit.get_info(topic)

        elif "play" in text and "online" in text:
            speak("What do you want me to play?")
            title = takecommand()
            print("playing {} in youtube".format(title))
            speak("playing {} in youtube".format(title))
            bot = music()
            bot.play(title)

        elif "go offline" in text:
            speak("Going offline sir")
            quit()
