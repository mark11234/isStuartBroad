import pandas as pd
import numpy as np
import requests
import lxml.html as lh
from bs4 import BeautifulSoup
import time

#Url to check, want to automate?
url = '''https://www.espncricinfo.com/series/new-zealand-in-england-2022-1276891/england-vs-new-zealand-3rd-test-1276903/live-cricket-score'''
isBatting = True
name = 'Stuart Broad'

while True:
    page = requests.get(url)
    if page.ok:
        content = page.content
        text = page.text

        doc = lh.fromstring(content)

        table = doc.xpath('//tr/td/span/a/span')
        #print(len(table))

        batter1 = table[0].text_content().split('*')[0]
        batter2 = table[1].text_content().split('(')[0]

        bob = table[1].text_content().split('(')[1]
        bat = bob == 'lhb)' or bob== 'rhb)'
        
        
        batter2 = batter2.strip()
        
        wasBatting = isBatting
        isBatting = batter1 == name or (batter2 == name and bat)
        
        if isBatting != wasBatting:
            if isBatting:
                print(name + ' is now batting')
            else:
                print(name + ' is no longer batting')

        time.sleep(5)
