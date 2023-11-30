# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 12:00:30 2023

@author: Eddie
"""

import requests
import chess
import random

headers = {'User-Agent': 'username: Takin_These, email: kenbarron@gmail.com'}
URL = 'https://api.chess.com/pub/player/hikaru/games/archives'

data = requests.get(URL, headers=headers)
print('data='+ str(data.status_code))
datajson=data.json()

hikaruGames = []
for index,url in enumerate(reversed(datajson['archives'])):
    #print (url)
    currentGames = requests.get(url,headers=headers).json()
    for game in currentGames['games']:
        thisGameData = {
            'white' : game['white'],
            'black' : game['black']
            }
        if game['time_class']=='blitz':
            hikaruGames.append(thisGameData)
    if index == 11:
        break

def simulate (gameSet):
    winRecord = []
    for game in gameSet:
        if game['white']['username']=='Hikaru':
            winChance = glickoCalculateWinChance(game['white']['rating'], game['black']['rating'])
            if random.uniform(0,1)<winChance:
                winRecord.append('win')
            else:
                winRecord.append('lose')
        else:
            winChance = glickoCalculateWinChance(game['black']['rating'], game['white']['rating'])
            if random.uniform(0,1)<winChance:
                winRecord.append('win')
            else:
                winRecord.append('lose')
    return winRecord

def glickoCalculateWinChance(rating1,rating2):
    return 1/(1+10**-((rating1-rating2)/400))