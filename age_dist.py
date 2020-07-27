# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 13:11:06 2020

@author: Nadav
"""

import numpy as np


def getAge(prob,city):
    if city == 'general':
        general_probs = np.array([0.095632, 0.311932, 0.669727, 0.777685, 0.858517, 1] )
        general = {0: [0,6] ,
                   1: [6,19], 
                   2: [19,46], 
                   3: [46,56], 
                   4: [56,65], 
                   5: [65,101]}
        return general[max(0,np.argmax(general_probs > prob)-1)]
    
    elif city == 'bnei_brak':
        bnei_brak_probs = np.array([0.17092,  0.468832, 0.806793, 0.8678,   0.915801, 1])
        bnei_brak = {0: [0,6] ,
                     1: [6,19], 
                     2: [19,46], 
                     3: [46,56], 
                     4: [56,65], 
                     5: [65,101]}
        return bnei_brak[max(0,np.argmax(bnei_brak_probs > prob)-1)]
    
    elif city == 'tel_aviv':
        tel_aviv_probs = np.array([0.065733, 0.190509, 0.592818, 0.711053, 0.801102, 1])
        tel_aviv = {0: [0,6] ,
                    1: [6,19], 
                    2: [19,46], 
                    3: [46,56], 
                    4: [56,65], 
                    5: [65,101]}
        return tel_aviv[max(0,np.argmax(tel_aviv_probs > prob)-1)]
    
    elif city == 'jerusalem':
        jerusalem_probs= np.array([0.118736, 0.372256, 0.731507, 0.818106, 0.88629,  1])
        jerusalem = {0: [0,6] ,
                     1: [6,19], 
                     2: [19,46], 
                     3: [46,56], 
                     4: [56,65], 
                     5: [65,101]}
        return jerusalem[max(0,np.argmax(jerusalem_probs > prob)-1)]   
    return np.random.randint(high=101)

