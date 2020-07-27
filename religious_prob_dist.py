# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 13:11:06 2020

@author: Nadav
"""

import numpy as np


def getVoteProb(city):
    
    prob = [4.56245926633418, 86.8150400228023, 4.07634070574229, 36.7813416862836]
    
    if city == 'general':
        city_prob = prob[0]/100 
        return city_prob
    
    elif city == 'bnei_brak':
        city_prob = prob[1]/100
        return city_prob
    
    elif city == 'tel_aviv':
        city_prob = prob[2]/100
        return city_prob
    
    elif city == 'jerusalem':
        city_prob = prob[3]/100
        return city_prob