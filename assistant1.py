import webbrowser  #to access any website
import pyttsx3     #to take speech output
import wikipedia   #to access information on wikipedia
import datetime
import speech_recognition as sr #to give input as speech
import os
import random
import smtplib   #for sending emails




#microsoft speech api to get the voice for the assistant
engine=pyttsx3.init('sapi5')
voices=engine.getProperty("voices")

#print(voices[1].id)
engine.setProperty("voice",voices[1].id)

def wish():
    '''When program starts assistant wishes the user'''
    Time=int(datetime.datetime.now().hour)
    if Time>=0 and Time<12:
        speak("Good Morning")
    elif Time>=12 and Time<17:
        speak('Good Afternoon')
    else:
        speak('Good Evening')
    speak('I am your Desktop Voice Assistant How may I help you')

def sendemail(to,content):
    '''To send Emails'''
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
        r.energy_threshold=300
        audio=r.listen(source)

    try:
        print('Interpreting')
        query=r.recognize_google(audio,language="en-in")
        print(query)
    except:
        print('Say that again please')
        return "None"
    return query

if __name__== '__main__':
    #directory with all the email IDs
    email={"Name1":"Name@gmail.com","Name2":"Name2@gmail.com"}
    wish()
    while True:
        #taking speech input from the user
        query=command().lower()
        #logic for executing tasks

        #to access info on wikipedia
        if "wikipedia" in query:
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



        #to open youtube
        elif "open youtube" in query:
            webbrowser.open(f"youtube.com")
        #to open google
        elif "open google" in query:
            webbrowser.open(f"google.com")

        #to create a text file
        elif "file" in query:
            speak('What will be the name of the file')
            name=command()
            fhand=open(f"{name}.txt",'w')
            speak('What do you want to write')
            text=command()
            fhand.write(text)
            fhand.close()
            speak('File created')



        #to play music
        elif "play music" in query:
            music_dir="Path of the file in which your songs are present on the computer can be provided here"
            songs=os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,random.choice(songs)))
        #to find out current time
        elif " the time" in query:
            strtime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strtime}")

        #to send an email
        elif "send email" in query:
            try:
                speak('What should I say')
                content=command()
                speak('Who should I send it to')
                to_name=command()
                if to_name in email:
                    to=email[to_name]
                    sendemail(to,content)
                else:
                    print('No such name found')
                speak('Email has been sent')
            except:
                speak('Sorry ,was not able to send the email')
        #to stop the assistant
        speak('Do you wish to continue please say Yes or No')
        ans=command()
        if "no" in ans.lower():
          speak('Thank you')
          break
