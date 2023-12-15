# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 12:00:30 2023

@author: Eddie
"""

import requests
import chess
import random
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial as poly

def CalculateDrawChance (gameSet):
    winDrawDistribution = []
    maxDifference = 0
    for game in gameSet:
        ratingDifference = abs(game['white']['rating']-game['black']['rating'])
        while (ratingDifference - maxDifference >= 0):
            maxDifference +=30
            winDrawDistribution.append([maxDifference,0,0,0])
        if game['white']['result']=='win' or game['black']['result']=='win':
            winDrawDistribution[ratingDifference // 30 ][1]+=1
        else:
            winDrawDistribution[ratingDifference // 30 ][2]+=1
    firstIntervalNoDrawsOrNoWins=0
    for i, interval in enumerate(winDrawDistribution):
        if interval[1]==0:
            firstIntervalNoDrawsOrNoWins = i
            break
        interval[3]=interval[1]/(interval[1]+interval[2])
        if interval[2]==0:
            firstIntervalNoDrawsOrNoWins = i+1
            break
    winDrawDistribution = winDrawDistribution[:firstIntervalNoDrawsOrNoWins]
    arrayFormat = np.array(winDrawDistribution)
    plt.plot(arrayFormat[:,0], arrayFormat[:,3])
    bestFit = poly.fit(arrayFormat[:,0], arrayFormat[:,3], 2)
    print(bestFit)
    x_poly, y_poly = bestFit.linspace()
    plt.plot(x_poly, y_poly)
    plt.show()
    return winDrawDistribution

def Simulate (gameSet):
    winRecord = []
    for game in gameSet:
        if game['white']['username']=='Hikaru':
            winChance = GlickoCalculateWinChance(game['white']['rating'], game['black']['rating'])
            if random.uniform(0,1)<winChance:
                winRecord.append('win')
            else:
                winRecord.append('lose')
        else:
            winChance = GlickoCalculateWinChance(game['black']['rating'], game['white']['rating'])
            if random.uniform(0,1)<winChance:
                winRecord.append('win')
            else:
                winRecord.append('lose')
    return winRecord

def GlickoCalculateWinChance(rating1,rating2):
    return 1/(1+10**-((rating1-rating2)/400))

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
        if game['time_class']=='blitz':
            thisGameData = {
            'white' : game['white'],
            'black' : game['black']
            }
            hikaruGames.append(thisGameData)
    if index == 11:
        break

winDrawChances = CalculateDrawChance (hikaruGames)
results = Simulate(hikaruGames)

