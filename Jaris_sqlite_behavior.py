#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Requires PyAudio and PySpeech.

import speech_recognition as sr
from gtts import gTTS
import os
import sqlite3
import subprocess
import webbrowser
import numpy as np

# database

# connect to the database file
conn = sqlite3.connect('example.db')
# create a cursor object to implement execute method
c = conn.cursor()


def read_from_db(command):
    # 因為python使用上
    # 也是透過 execute("...") 在 sqlite 自己的terminal 上輸入指令
    # 所以 "..." 的內容是 SELECT * FROM JarvisCommand WHERE INSTR('turn on the light', keyword)
    # 而 字串代換的過程中 如果沒有在 %s 旁加上 '' 會變成 SELECT * FROM JarvisCommand WHERE INSTR(turn on the light, keyword)
    # 不符合規則！
    c.execute("SELECT * FROM JarvisCommand WHERE INSTR('%s', keyword)" % command)
    # data is an array
    data = c.fetchall()
    #print data
    return data


# Record Audio
r = sr.Recognizer()

from pynput.keyboard import Key, Listener
def on_press(key):
    print('{0} pressed'.format(
        key))
    if key == Key.enter:
        # Stop listener
        return False

while True:
    with sr.Microphone() as source:
        
        raw_input('press enter')
        r.adjust_for_ambient_noise(source) #CENTOS ONLY
        
        audio = r.listen(source)

        # get the data frame from audio
        s=audio.frame_data
        b=bytearray(s)

        print "frame length : "+str(len(b))

    if len(b)>1000000: print "frame size too large, pass it"

    elif np.count_nonzero(b)*0.56 > len(b)-np.count_nonzero(b):
        print "nonzero more"
        # Speech recognition using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            text = r.recognize_google(audio)
            print(text)

            action = read_from_db(text)
            print(action)

            if len(action) != 0:

                if action[0][2] != None:
                    answer = action[0][2]

                if action[0][1] != ' ':  # I use space to express nothing in sqlite
                    print(action[0][1])
                    #os.system("python ./behavior/"+action[0][1])
                    pid = subprocess.Popen(["python", "./behavior/"+action[0][1]])

                if answer != ' ':
                    tts = gTTS(text=answer, lang='en')
                    # tts = gTTS(text='chen bo shium chou gay', lang='en')
                    tts.save("1.mp3")
                    os.system("mpg123 1.mp3 -quiet")

        except sr.UnknownValueError:
            print("----------")
        except sr.RequestError as e:
            print(
                "Could not request results from Google Speech Recognition service; {0}".format(e))

    else:
        print "zero more"
