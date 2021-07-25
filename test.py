import pyttsx3
import random
import speech_recognition as sound
from collections import deque
import wikipedia
import datetime
import mediapipe as mp
import math
import autopy
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
        elif 'activate super mode' or 'remote mouse' in query:
            class handDetector():
                def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
                    self.mode = mode
                    self.maxHands = maxHands
                    self.detectionCon = detectionCon
                    self.trackCon = trackCon

                    self.mpHands = mp.solutions.hands
                    self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
                    self.mpDraw = mp.solutions.drawing_utils
                    self.tipIds = [4, 8, 12, 16, 20]

                def findHands(self, img, draw=True):
                    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    self.results = self.hands.process(imgRGB)
                    # print(results.multi_hand_landmarks)
                    if self.results.multi_hand_landmarks:
                        for handLms in self.results.multi_hand_landmarks:
                            if draw:
                                self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

                    return img

                def findPosition(self, img, handNo=0, draw=True):
                    xList = []
                    yList = []
                    bbox = []
                    self.lmList = []
                    if self.results.multi_hand_landmarks:
                        myHand = self.results.multi_hand_landmarks[handNo]
                        for id, lm in enumerate(myHand.landmark):
                            # print(id, lm)
                            h, w, c = img.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            xList.append(cx)
                            yList.append(cy)
                            # print(id, cx, cy)
                            self.lmList.append([id, cx, cy])
                            if draw:
                                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                        xmin, xmax = min(xList), max(xList)
                        ymin, ymax = min(yList), max(yList)
                        bbox = xmin, ymin, xmax, ymax
                        if draw:
                            cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20), (0, 255, 0), 2)
                    return self.lmList, bbox

                def fingersUp(self):
                    fingers = []
                    if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                    for id in range(1, 5):

                        if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    return fingers

                def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
                    x1, y1 = self.lmList[p1][1:]
                    x2, y2 = self.lmList[p2][1:]
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    if draw:
                        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
                        cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
                        cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
                        cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
                    length = math.hypot(x2 - x1, y2 - y1)
                    return length, img, [x1, y1, x2, y2, cx, cy]
            def main():
                wCam, hCam = 640, 480
                frameR = 100
                smoothening = 10
                plocX, plocY = 0, 0
                clocX, clocY = 0, 0
                pTime = 0
                cTime = 0
                cap = cv2.VideoCapture(0)
                cap.set(3, wCam)
                cap.set(4, hCam)
                detector = handDetector()
                wScr, hScr = autopy.screen.size()
                print(wScr, hScr)
                while True:
                    success, img = cap.read()
                    img = detector.findHands(img)
                    lmList, bbox = detector.findPosition(img)
                    if len(lmList) != 0:
                        x1, y1 = lmList[8][1:]
                        x2, y2 = lmList[12][1:]
                        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
                        print(x1, y1, x2, y2)
                        fingers = detector.fingersUp()
                        print(fingers)
                        if fingers[1] == 1 and fingers[2] == 0:
                            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                            clocX = plocX + (x3 - plocX) / smoothening
                            clocY = plocY + (y3 - plocY) / smoothening
                            pyautogui.moveTo(wScr - clocX, clocY)
                            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                            plocX, plocY = clocX, clocY
                        if fingers[1] == 1 and fingers[2] == 1:
                            length, img, lineInfo = detector.findDistance(8, 12, img)
                            print(length)
                            if length < 40:
                                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                                pyautogui.click()
                    cTime = time.time()
                    fps = 1 / (cTime - pTime)
                    pTime = cTime
                    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                    cv2.imshow("Image", img)
                    cv2.waitKey(1)
            main()
        elif 'i wanna draw' or 'draw' in query:
            blueLower = np.array([100, 60, 60])
            blueUpper = np.array([140, 255, 255])
            kernel = np.ones((5, 5), np.uint8)
            bpoints = [deque(maxlen=512)]
            gpoints = [deque(maxlen=512)]
            rpoints = [deque(maxlen=512)]
            ypoints = [deque(maxlen=512)]
            bindex = 0
            gindex = 0
            rindex = 0
            yindex = 0

            colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (0, 0, 0)]
            colorIndex = 0

            paintWindow = np.zeros((471, 636, 3)) + 255
            paintWindow = cv2.rectangle(paintWindow, (40, 1), (140, 65), (0, 0, 0), 2)
            paintWindow = cv2.rectangle(paintWindow, (160, 1), (255, 65), colors[0], -1)
            paintWindow = cv2.rectangle(paintWindow, (275, 1), (370, 65), colors[1], -1)
            paintWindow = cv2.rectangle(paintWindow, (390, 1), (485, 65), colors[2], -1)
            paintWindow = cv2.rectangle(paintWindow, (505, 1), (600, 65), colors[3], -1)
            cv2.putText(paintWindow, "ERASE", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(paintWindow, "RED", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(paintWindow, "GREEN", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(paintWindow, "BLACK", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)

            cv2.namedWindow('PAINT', cv2.WINDOW_AUTOSIZE)

            camera = cv2.VideoCapture(0)
            while True:

                (grabbed, frame) = camera.read()
                frame = cv2.flip(frame, 1)
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                # Add the coloring options to the frame
                frame = cv2.rectangle(frame, (40, 1), (140, 65), (122, 122, 122), -1)
                frame = cv2.rectangle(frame, (160, 1), (255, 65), colors[0], -1)
                frame = cv2.rectangle(frame, (275, 1), (370, 65), colors[1], -1)
                frame = cv2.rectangle(frame, (390, 1), (485, 65), colors[2], -1)
                frame = cv2.rectangle(frame, (505, 1), (600, 65), colors[3], -1)
                cv2.putText(frame, "ERASE", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, "RED", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, "GREEN", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, "BLACK", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 2, cv2.LINE_AA)
                if not grabbed:
                    break
                blueMask = cv2.inRange(hsv, blueLower, blueUpper)
                blueMask = cv2.erode(blueMask, kernel, iterations=2)
                blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
                blueMask = cv2.dilate(blueMask, kernel, iterations=1)

                cnts, _ = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                center = None
                if len(cnts) > 0:
                    cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
                    ((x, y), radius) = cv2.minEnclosingCircle(cnt)
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                    M = cv2.moments(cnt)
                    center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

                    if center[1] <= 65:
                        if 40 <= center[0] <= 140:  # Clear All
                            bpoints = [deque(maxlen=512)]
                            gpoints = [deque(maxlen=512)]
                            rpoints = [deque(maxlen=512)]
                            ypoints = [deque(maxlen=512)]

                            bindex = 0
                            gindex = 0
                            rindex = 0
                            yindex = 0

                            paintWindow[67:, :, :] = 255
                        elif 160 <= center[0] <= 255:
                            colorIndex = 0  # Blue
                        elif 275 <= center[0] <= 370:
                            colorIndex = 1  # Green
                        elif 390 <= center[0] <= 485:
                            colorIndex = 2  # Red
                        elif 505 <= center[0] <= 600:
                            colorIndex = 3  # Yellow
                    else:
                        if colorIndex == 0:
                            bpoints[bindex].appendleft(center)
                        elif colorIndex == 1:
                            gpoints[gindex].appendleft(center)
                        elif colorIndex == 2:
                            rpoints[rindex].appendleft(center)
                        elif colorIndex == 3:
                            ypoints[yindex].appendleft(center)
                else:
                    bpoints.append(deque(maxlen=512))
                    bindex += 1
                    gpoints.append(deque(maxlen=512))
                    gindex += 1
                    rpoints.append(deque(maxlen=512))
                    rindex += 1
                    ypoints.append(deque(maxlen=512))
                    yindex += 1
                points = [bpoints, gpoints, rpoints, ypoints]
                for i in range(len(points)):
                    for j in range(len(points[i])):
                        for k in range(1, len(points[i][j])):
                            if points[i][j][k - 1] is None or points[i][j][k] is None:
                                continue
                            cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                            cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.imshow("CAMERA", frame)
                cv2.imshow("Drawing screen", paintWindow)
                print(paintWindow)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

            camera.release()
            cv2.destroyAllWindows()
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