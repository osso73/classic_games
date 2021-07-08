#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 20:18:10 2021

@author: oriol
"""

import os


SPEED = 0.25
GRID_SIZES = [11, 15, 19, 23]
SPEED_FACTORS = [0.5, 0.8, 1, 1.5, 2, 3]
MINIMUM_SWIPE = 50
IMAGES = os.path.join(os.path.dirname(__file__), 'images')  # path of images
URL_HELP = 'https://osso73.github.io/classic_games/games/classic_games/#game-of-snake'
FOOD_SPEED = 1.5
FOOD_SPEED_TIME = 20
INITIAL_SNAKE_LENGTH = 3  # length of the snake when starting the level

FOOD_PARAMETERS = {
    'fruit': {'speed': 1, 'score': 3, 'length': 1},
    'junk':  {'speed': FOOD_SPEED, 'score': 1, 'length': 2},
    'sweet': {'speed': 1, 'score': 1, 'length': 3},
    }

LEVEL_PARAMETERS = {  # parameters for vertical layout
    1: {'pos_ini': (0.5, 0.5), 'dir': 'DOWN'},
    2: {'pos_ini': (0.5, 0.75), 'dir': 'RIGHT'},
    3: {'pos_ini': (0.25, 0.5), 'dir': 'DOWN'},
    4: {'pos_ini': (0.5, 0.5), 'dir': 'RIGHT'},
    5: {'pos_ini': (0.5, 0.5), 'dir': 'DOWN'},
    6: {'pos_ini': (0.15, 0.5), 'dir': 'DOWN'},
    7: {'pos_ini': (0.15, 0.5), 'dir': 'DOWN'},
    8: {'pos_ini': (0.5, 0.5), 'dir': 'DOWN'},
    9: {'pos_ini': (0.25, 0.5), 'dir': 'DOWN'},
    10: {'pos_ini': (0.5, 0.5), 'dir': 'RIGHT'},
    11: {'pos_ini': (0.2, 0.5), 'dir': 'DOWN'},
    12: {'pos_ini': (0.2, 0.5), 'dir': 'DOWN'},
    }
