import webbrowser  #to access any website
import pyttsx3     #to take speech output
import wikipedia   #to access information on wikipedia
import datetime
import speech_recognition as sr #to give input as speech
import os
import random
import smtplib #for emails
import pyautogui


class person:
    name = ''
    def setName(self, name):
        self.name = name

def there_exists(terms):
    for term in terms:
        if term in query:
            return True




#microsoft speech api to get the voice for the assistant
engine=pyttsx3.init('sapi5')
voices=engine.getProperty("voices")

#print(voices[1].id)
engine.setProperty("voice",voices[1].id)

def wish(name):
    '''When programs starts it wishes the user'''
    Time=int(datetime.datetime.now().hour)
    if Time>=0 and Time<12:
        speak("Good Morning")
    elif Time>=12 and Time<17:
        speak('Good Afternoon')
    else:
        speak('Good Evening')
    speak(f"Hello {name}  I am your Desktop Voice Assistant How may I help you")

def sendemail(to,content):
    '''To send emails'''
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.login("sender's gmail id","Your-password")
    server.sendmail("sender's gmail id",to,content)
    server.close()


def speak(audio):
    '''Makes the assistant give speech output for written input'''
    engine.say(audio)
    engine.runAndWait()

def command():
    '''Takes voice input from the user and returns string output'''
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold=2
        audio=r.listen(source)

    try:
        print('Interpreting')
        query=r.recognize_google(audio,language="en-in")
        print(query)
    except:
        print('Sorry did not get that')
        return "None"
    return query

if __name__== '__main__':
    #directory with all the email id
    personobj=person()
    email={"Name1":"Name@gmail.com","Name2":"Name2@gmail.com"}
    wish(personobj.name)
    while True:
        #taking speech input from the user
        query=command().lower()
        #logic for executing task

        if there_exists(['hey','hi','hello']):
            speak('How may I help you')
            continue

        #to access info on wikipedia
        elif there_exists(["wikipedia"]):
            speak('Searching wikipedia..')
            query=query.replace("wikipedia","")
            try:
                results=wikipedia.summary(query,sentences=2)
                speak('According to wikipedia')
                print(results)
                speak(results)
            except:
                print('Please say that again')
                continue
        elif there_exists(["capture","my screen","screenshot"]):
            myScreenshot = pyautogui.screenshot()
            myScreenshot.show()

        #greetings
        elif there_exists(["my name is"]):
            name=query.split("is")[-1]

            personobj.setName(name)
            speak("I will remember that now")

        elif there_exists(["what is your name","what's your name","tell me your name"]):
            speak("My name is Fexa")

        elif there_exists(["how are you","how are you doing"]):
            speak("I'm very well, thanks for asking " + personobj.name)

        #to open youtube
        elif there_exists(["youtube"]):
            webbrowser.open(f"youtube.com")


        elif there_exists(["search"]) and 'youtube' not in query:
            search_term = query.split()[-1]
            url = f"https://google.com/search?q={search_term}"
            webbrowser.get().open(url)
            speak(f'Here is what I found for {search_term} on google')

        #to create a text file
        elif there_exists(["create file"]):
            speak('What will be the name of the file')
            name=command()
            if name!="None":
                fhand=open(f"{name}.txt",'w')
                speak('What do you want to write')
                text=command()
                fhand.write(text)
                fhand.close()
                speak('File created')
            else:
                speak('Sorry could not understand file name')
                continue
        #calculator
        elif there_exists(["plus","minus","multiply","divide","power","+","-","*","/"]):
            op = query.split()[1]

            if op == '+':
                speak(int(query.split()[0]) + int(query.split()[2]))
            elif op == '-':
                speak(int(query.split()[0]) - int(query.split()[2]))
            elif op == 'multiply' or 'x':
                speak(int(query.split()[0]) * int(query.split()[2]))
            elif op == 'divide':
                speak(int(query.split()[0]) / int(query.split()[2]))
            elif op == 'power':
                speak(int(query.split()[0]) ** int(query.split()[2]))
            else:
                speak("Wrong Operator")



        #to play music
        elif there_exists(["play music"]):
            music_dir="Path of the file in which your songs are present on the computer can be provided here"
            songs=os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,random.choice(songs)))
        #to find out current time
        elif there_exists(["what's the time","tell me the time","what time is it","what is the time"]):
            strtime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strtime}")
        # current weather
        elif there_exists(["weather"]):

            #search_term = query.split("for")[-1]
            url = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q=weather&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
            webbrowser.get().open(url)
            speak("Here is what I found for on google")


        #to send an email
        elif there_exists(["send email"]):
            try:
                speak('What should I say')
                content=command()
                if content!="None":
                    speak('Who should I send it to')
                    to_name=command()
                    if to_name in email:
                        to=email[to_name]
                        sendemail(to,content)
                    else:
                        print('No such name found')
                else:
                    continue
                speak('Email has been sent')
            except:
                speak('Sorry ,was not able to send the email')

        elif there_exists(["exit", "quit", "goodbye"]):
            speak('Thank you')
            break
        else:
            speak('Sorry I could not find anything on this')
