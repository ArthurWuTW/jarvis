#!/usr/bin/env python
# -*- coding: utf8 -*-

import requests
from bs4 import BeautifulSoup
import time
import re
import os
import urllib
import json
import io

URL = 'https://www.taiwannews.com.tw/'
res = requests.get(URL)
soup = BeautifulSoup(res.text, 'html.parser')

divs = soup.find_all('article')

main_text = []

for d in divs:
    main_text.append(d.text.replace('\n', ' '))

for i in range(len(main_text)):
    if main_text[i] is None:
        main_text[i] = []

# ' '.join(array) -> string array to one string separated by ' '
with io.open('/home/arthur/Desktop/Speech_Recognize_Sqlite/JSON_file/news.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(main_text, ensure_ascii=False))

print("finish")
