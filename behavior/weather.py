#!/usr/bin/env python
import os
import json
from gtts import gTTS

print("this is weather.py!")

answer = ''

with open('./JSON_file/city_temp_precipitation.json', 'r') as f:
    text_array = json.load(f)
answer = 'well Sir, In ' + text_array[0]+', forecast temperature is from ' + \
    text_array[1] + \
    ' degrees, and rain possibility is '+text_array[2]
# say the word
tts = gTTS(text=answer, lang='en')

# avoid synchronization
tts.save("2.mp3")
os.system("mpg123 2.mp3 -quiet")
