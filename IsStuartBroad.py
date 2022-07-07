'''
Finds the current England cricket match, checks if it's live and finds
out whether Stuart Broad is batting.
ESPNcricinfo is for personal non-commercial home use only,
as stated at https://disneytermsofuse.com/english-united-kingdom/
[accessed 25th June 2022]
TO-DO:
-Check full range of values for matchStatus
-Find data for Nottingham/other cricket games too
'''
import pandas as pd
import numpy as np
import requests
import lxml.html as lh
import time
englandUrl = 'https://www.espncricinfo.com/team/england-1/match-schedule-fixtures'

page = requests.get(englandUrl)
content = page.content
doc = lh.fromstring(content)

#Finding the status of the game
elements = doc.xpath("//div[@class='ds-px-4 ds-py-3']/a/div/div/div/div/span[@class='ds-text-tight-xs ds-font-bold ds-uppercase ds-leading-5']")
matchStatus = elements[0].text_content()

#Check if the game is ongoing, possibly incomplete - need an exhaustive list
validGameStates = ['Live','Stumps','Lunch','Tea','Innings break']
liveMatch = False
for state in validGameStates:
    liveMatch = liveMatch or state == matchStatus
    if liveMatch:
        break
#Check if delayed, unsure if capitalised - need to check in rain delay
liveMatch = liveMatch or 'delayed' in matchStatus or 'Delayed' in matchStatus

if not(liveMatch):
    print('England Men are not playing')
else:
    #Find the URL of current game
    elements = doc.xpath("//div[@class='ds-px-4 ds-py-3']/a")
    url = 'https://www.espncricinfo.com/'+elements[0].attrib['href']
    
    isBatting = False
    firstTime = True
    name = 'Stuart Broad'
    while True:
        page = requests.get(url)
        if page.ok:
            content = page.content
            text = page.text
            doc = lh.fromstring(content)

            #Find the batters names in table & remove excess info
            table = doc.xpath('//tr/td/span/a/span')
            batter1 = table[0].text_content().split('*')[0]
            batter2 = table[1].text_content().split('(')[0]
            batter2 = batter2.strip()

            #Find out if batter
            bob = table[1].text_content().split('(')[1]
            bat = bob == 'lhb)' or bob== 'rhb)'

            #Check if batsman has changed
            wasBatting = isBatting
            isBatting = batter1 == name or (batter2 == name and bat)

            #Output accordingly
            if firstTime and isBatting:
                print(name, 'is batting')
            elif firstTime and not(isBatting):
                print(name, 'is not batting')
            elif isBatting != wasBatting:
                if isBatting:
                    print(name, 'is now batting')
                else:
                    print(name, 'is no longer batting')
            firstTime = False
            time.sleep(5) #Dont DOS cricinfo
