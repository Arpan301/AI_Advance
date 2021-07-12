import pyttsx3
import random
import speech_recognition as sound
import wikipedia
import datetime
import time
import getpass
import pywhatkit as kit
import webbrowser
import os
import cv2
import numpy as np
import pyautogui
import smtplib
webcam = cv2.VideoCapture(0)
username = getpass.getuser()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def takeinput():
    r = sound.Recognizer()
    with sound.Microphone() as source:
        print("Say something....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception :
        print("Say that again please...")
        return "None"
    return query

def send(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('arpanroy@gg.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()
def arunavo():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")
    time.sleep(2)
    nam= username+ " ,what can i do for u"
    speak(nam)
remember="arpan"
if __name__ == "__main__":
    arunavo()
    while True:
        query = takeinput().lower()
        if 'what is meant' in query or 'stands for' in query or 'what is the meaning of' in query:
            speak('Searching..')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=5)
            speak("According to Wikipedia")
            print(results)
            speak(results)
            time.sleep(1)
            speak('if u think this does not match your answer try saying search for')
        elif 'open youtube and play the song' in query:
            zr=query.split(" ")
            a = zr[6::]
            z = ' '.join([str(elem) for elem in a])
            speak(f"playing,  {z}")
            kit.playonyt(z)
            break
        elif 'open youtube and play ' in query:
            try:
                zz=query.split(" ")
                a = zz[4::]
                z = ' '.join([str(elem) for elem in a])
                speak(f"playing,  {z}")
                kit.playonyt(z)
            except Exception:
                print("u don't have youtube lol")
                speak("u don't have youtube lol")
            break
        elif 'youtube' in query:
            zo=query
            kit.playonyt(zo)
            break
        elif 'search for' in query:
            kk=query.split(" ")
            aa=kk[2::]
            zx = ' '.join([str(elem) for elem in aa])
            kit.search(zx)
        elif '.com' in query:
            try:
                ss = query.split(" ")
                dd = ss[1::]
                zc = ' '.join([str(elem) for elem in dd])
                webbrowser.register('brave', None, webbrowser.BackgroundBrowser("C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"))
                webbrowser.get('brave').open(zc)
                while (1):
                    _, imageFrame = webcam.read()
                    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
                    green_lower = np.array([25, 52, 72], np.uint8)
                    green_upper = np.array([102, 255, 255], np.uint8)
                    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
                    blue_lower = np.array([94, 80, 2], np.uint8)
                    blue_upper = np.array([120, 255, 255], np.uint8)
                    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
                    kernal = np.ones((5, 5), "uint8")
                    green_mask = cv2.dilate(green_mask, kernal)
                    res_green = cv2.bitwise_and(imageFrame, imageFrame, mask=green_mask)
                    blue_mask = cv2.dilate(blue_mask, kernal)
                    res_blue = cv2.bitwise_and(imageFrame, imageFrame,mask=blue_mask)
                    contours, hierarchy = cv2.findContours(green_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                    for pic, contour in enumerate(contours):
                        area = cv2.contourArea(contour)
                        if (area > 10000):
                            pyautogui.hotkey('shift','space')
                    contours, hierarchy = cv2.findContours(blue_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                    for pic, contour in enumerate(contours):
                        area = cv2.contourArea(contour)
                        if (area > 10000):
                            pyautogui.press('space')
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        break
            except Exception:
                print("set your browser")
                speak("set your browser")
            break
        elif 'play music' in query:
            try:
                music_dir = 'C:\\Users\\Arpan roy\\AppData\\Local\\Microsoft\\WindowsApps\\SpotifyAB.SpotifyMusic_zpdnekdrzrea0\\Spotify.exe'
                os.startfile(music_dir)
            except Exception:
                print("spotify is not installed try on youtube")
                speak("spotify is not installed try on youtube")
            break
        elif 'what is the time' in query or 'what is the time right now' in query or 'time right now' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif 'open windows 7' in query:
            try:
                homedir = os.path.expanduser("~")
                codePath = "\\VirtualBox VMs\\windows 7\\windows 7.vbox"
                os.startfile(homedir+codePath)
            except Exception:
                print("u don't have windows 7")
                speak("u don't have windows 7")
            break
        elif 'open metasploitable 2' in query:
            try:
                homedir = os.path.expanduser("~")
                codePath = "\\VirtualBox VMs\\metasploitable 2\\metasploitable 2.vbox"
                os.startfile(homedir+codePath)
            except Exception:
                print("u don't have metasploitable in your machine")
                speak("u don't have metasploitable in your machine")
            break
        elif 'open windows 10' in query:
            try:
                homedir = os.path.expanduser("~")
                codePath = "\\VirtualBox VMs\\windows 10\\windows 10.vbox"
                os.startfile(homedir+codePath)
            except Exception:
                print("you don't have windows 10 on virtual box")
                speak("you don't have windows 10 on virtual box")
            break
        elif 'open kali linux' in query:
            try:
                homedir = os.path.expanduser("~")
                codePath = "\\VirtualBox VMs\\kali\\kali.vbox"
                os.startfile(homedir+codePath)
            except Exception:
                print("you don't have kali on virtual box")
                speak("you don't have kali on virtual box")
            break
        elif 'open centos' in query:
            try:
                homedir = os.path.expanduser("~")
                codePath = "\\VirtualBox VMs\\CentOS_8.3.2011_VBM_LinuxVMImages.COM\\CentOS_8.3.2011_VBM_LinuxVMImages.COM.vbox"
                os.startfile(homedir+codePath)
            except Exception:
                print("you don't have centos on virtual box")
                speak("you don't have centos 10 on virtual box")
            break
        elif 'tell me a joke' in query or 'say me a joke' in query or 'say a joke' in query or 'tell a joke' in query:
            a = "What can coronavirus do that the United States government can’t? Stop school shootings."
            b = "I told my therapist that I am having suicidal thoughts, He now makes me pay in advance."
            cd="Why don’t Calculus majors throw house parties? Because you should never drink and derive."
            d="What’s orange and sounds like a carrot? A parrot."
            e="What do you call a magic dog? A labracadabrador."
            lis = [a, b,cd,d,e]
            item = random.choice(lis)
            print(item)
            speak(item)
            break
        elif 'sing me a song' in query or 'sing a song' in query or 'sing a song for me' in query:
            azz='Blackbird singing in the dead of nightTake these broken wings and learn to flyAll your life You were only waiting for this moment to arise'
            bzz='Always take a big bite It’s such a gorgeous sightTo see you eat in the middle of the night'
            czz='Take me into your loving arms Kiss me under the light of a thousand stars Place your head on my beating heart'
            ll= [azz,bzz,czz]
            itt=random.choice(ll)
            print(itt)
            speak(itt)
            break
        elif 'what can you do' in query:
            print("i can do everything, just try me")
            speak("i can do everything, just try me")
            break
        elif 'email to' in query:
            try:
                speak("What should I write in email")
                sp=input("enter what u want to send")
                to = "arpan@gmail.com"
                send("arpanroy@nsec.in", sp)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry darling arpan , please sent the email by yourself")
            break
        elif 'open profile in ' in query:
            try:
                ssd = query.split(" ")
                dde =ssd[3:4:]
                name=ssd[5::]
                zl = ' '.join([str(elem) for elem in dde])
                web=zl+".com"
                kc=' '.join([str(ele) for ele in name])
                webbrowser.register('brave', None, webbrowser.BackgroundBrowser("C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"))
                webbrowser.get('brave').open(web)
                speak("opening profile")
                time.sleep(6)
                pyautogui.press('/')
                pyautogui.typewrite(kc)
                pyautogui.press('enter')
                while (1):
                    _, imageFrame = webcam.read()
                    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
                    green_lower = np.array([25, 52, 72], np.uint8)
                    green_upper = np.array([102, 255, 255], np.uint8)
                    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
                    blue_lower = np.array([94, 80, 2], np.uint8)
                    blue_upper = np.array([120, 255, 255], np.uint8)
                    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
                    kernal = np.ones((5, 5), "uint8")
                    green_mask = cv2.dilate(green_mask, kernal)
                    res_green = cv2.bitwise_and(imageFrame, imageFrame, mask=green_mask)
                    blue_mask = cv2.dilate(blue_mask, kernal)
                    res_blue = cv2.bitwise_and(imageFrame, imageFrame, mask=blue_mask)
                    contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    for pic, contour in enumerate(contours):
                        area = cv2.contourArea(contour)
                        if (area > 10000):
                            pyautogui.hotkey('shift', 'space')
                    contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    for pic, contour in enumerate(contours):
                        area = cv2.contourArea(contour)
                        if (area > 10000):
                            pyautogui.press('space')
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        break
            except Exception:
                speak("i am having problem...solve it yourself")
                print("i am having problem...solve it yourself")
            break
        elif 'remember' in query:
            rem=query.split(" ")
            pi = rem[1::]
            remember= ' '.join([str(elem) for elem in pi])
            speak("ok...i will remember that")
            break
        elif 'say what i told you to remember' in query:
            speak(remember)
            break
        elif "none" in query:
            if len(query) > 4:
                speak("i found this on google")
                kit.search(query)
                while (1):
                    _, imageFrame = webcam.read()
                    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
                    green_lower = np.array([25, 52, 72], np.uint8)
                    green_upper = np.array([102, 255, 255], np.uint8)
                    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
                    blue_lower = np.array([94, 80, 2], np.uint8)
                    blue_upper = np.array([120, 255, 255], np.uint8)
                    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
                    kernal = np.ones((5, 5), "uint8")
                    green_mask = cv2.dilate(green_mask, kernal)
                    res_green = cv2.bitwise_and(imageFrame, imageFrame, mask=green_mask)
                    blue_mask = cv2.dilate(blue_mask, kernal)
                    res_blue = cv2.bitwise_and(imageFrame, imageFrame,mask=blue_mask)
                    contours, hierarchy = cv2.findContours(green_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                    for pic, contour in enumerate(contours):
                        area = cv2.contourArea(contour)
                        if (area > 10000):
                            pyautogui.hotkey('shift','space')
                    contours, hierarchy = cv2.findContours(blue_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                    for pic, contour in enumerate(contours):
                        area = cv2.contourArea(contour)
                        if (area > 10000):
                            pyautogui.press('space')
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        break
            else:
                continue
            break
        else:
            speak("i found this on google")
            kit.search(query)
            while (1):
                _, imageFrame = webcam.read()
                hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
                green_lower = np.array([25, 52, 72], np.uint8)
                green_upper = np.array([102, 255, 255], np.uint8)
                green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
                blue_lower = np.array([94, 80, 2], np.uint8)
                blue_upper = np.array([120, 255, 255], np.uint8)
                blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)
                kernal = np.ones((5, 5), "uint8")
                green_mask = cv2.dilate(green_mask, kernal)
                res_green = cv2.bitwise_and(imageFrame, imageFrame, mask=green_mask)
                blue_mask = cv2.dilate(blue_mask, kernal)
                res_blue = cv2.bitwise_and(imageFrame, imageFrame, mask=blue_mask)
                contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if (area > 10000):
                        pyautogui.hotkey('shift', 'space')
                contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if (area > 10000):
                        pyautogui.press('space')
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
            break