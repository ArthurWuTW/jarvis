#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from gtts import gTTS

print("this is news.py")

answer = ''

# './JSON_file/news.json' 的 path 是以 Jarvis_splite_behavior 作為 root path!!
with open('./JSON_file/news.json', 'r') as f:
    text_array = json.load(f)
answer = 'Sir, here are'+str(len(text_array))+' news, '+' '.join(text_array)
# say the word
tts = gTTS(text=answer, lang='en')

# avoid synchronization
tts.save("2.mp3")
os.system("mpg123 2.mp3 -quiet")
