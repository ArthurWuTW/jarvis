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

URL = 'https://www.cwb.gov.tw/V7e/forecast/taiwan/Kaohsiung_City.htm'
res = requests.get(URL)
soup = BeautifulSoup(res.text, 'html.parser')

main_text = []

# divs[0] ...

#<table class="FcstBoxTable01" summary="Layout Purpose">\n<thead>\n<tr>\n<th width="25%">Kaohsiung City</th>\n<th width="19%">Temperature (\xe2\x84\x83)</th>\n
# <th width="13%">Weather</th>\n<th width="19%">Comfort index</th>\n<th width="25%">Probability of Precipitation (%)</th>\n</tr>
# \n</thead>\n<tbody><tr>\n<th scope="row">Tonight 06/18 00:00~06/18 06:00</th>\n<td>26 ~ 27</td>\n<td>\n
# <img alt="CLOUDY WITH SHOWERS OR THUNDERSTORMS" src="../../symbol/weather/gif/night/31.gif" title="CLOUDY WITH SHOWERS OR THUNDERSTORMS"/></td>
# \n<td>COMFORTABLE</td>\n<td>80 %</td>\n</tr><tr>\n<th scope="row">Tomorrow 06/18 06:00~06/18 18:00</th>\n<td>26 ~ 29</td>\n<td>\n
# <img alt="MOSTLY CLOUDY WITH SHOWERS OR THUNDERSTORMS" src="../../symbol/weather/gif/day/36.gif" title="MOSTLY CLOUDY WITH SHOWERS OR THUNDERSTORMS"/>
# </td>\n<td>COMFORTABLE~HOT</td>\n<td>80 %</td>\n</tr><tr>\n<th scope="row">Tomorrow Night 06/18 18:00~06/19 06:00</th>\n<td>27 ~ 28</td>
# \n<td>\n<img alt="MOSTLY CLOUDY WITH SHOWERS OR THUNDERSTORMS" src="../../symbol/weather/gif/night/36.gif" title="MOSTLY CLOUDY WITH SHOWERS OR THUNDERSTORMS"/></td>
# \n<td>COMFORTABLE~HOT</td>\n<td>80 %</td>\n</tr></tbody>\n</table>


divs = soup.find_all('table')
divs_1 = divs[0].find_all('th')
divs_2 = divs[0].find_all('td')

main_text.append(divs_1[0].string)  # Kaoshiung City

# >>> divs[0].find_all('td')[4]
# <td>26 ~ 29</td>
main_text.append(divs_2[4].string.replace('~', 'to'))

# >>> divs[0].find_all('td')[7]
# <td>80 %</td>
main_text.append(divs_2[7].string)

with io.open('/home/arthur/Desktop/Speech_Recognize_Sqlite/JSON_file/city_temp_precipitation.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(main_text, ensure_ascii=False))

print("finish")
