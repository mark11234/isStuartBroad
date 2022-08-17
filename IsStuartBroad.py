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
england_url = 'https://www.espncricinfo.com/team/england-1/match-schedule-fixtures'

page = requests.get(england_url)
content = page.content
doc = lh.fromstring(content)

#Finding the status of the game
elements = doc.xpath("//div[@class='ds-px-4 ds-py-3']/a/div/div/div/div/span[@class='ds-text-tight-xs ds-font-bold ds-uppercase ds-leading-5']")
match_status = elements[0].text_content()

valid_game_states = ['Live','Stumps','Lunch','Tea','Innings break']
live_match = False
for state in valid_game_states:
    live_match = live_match or state == match_status
    if live_match:
        break
# TODO: check which is needed during a rain delay
live_match = live_match or 'delayed' in match_status or 'Delayed' in match_status

if not(live_match):
    print('England Men are not playing')
else:
    #Find the URL of current game
    elements = doc.xpath("//div[@class='ds-px-4 ds-py-3']/a")
    url = 'https://www.espncricinfo.com/'+elements[0].attrib['href']
    
    is_batting = False
    first_time = True
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

            batter2_batter_or_bowler_type = table[1].text_content().split('(')[1]
            batter2_is_batter = batter2_batter_or_bowler_type == 'lhb)' or batter2_batter_or_bowler_type== 'rhb)'

            wasBatting = is_batting
            is_batting = batter1 == name or (batter2 == name and batter2_is_batter)

            if first_time and is_batting:
                print(name, 'is batting')
            elif first_time and not(is_batting):
                print(name, 'is not batting')
            elif is_batting != wasBatting:
                if is_batting:
                    print(name, 'is now batting')
                else:
                    print(name, 'is no longer batting')
            first_time = False
            time.sleep(5) #Dont DOS cricinfo
