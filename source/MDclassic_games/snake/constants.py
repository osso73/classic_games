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
HELP_URL = 'https://osso73.github.io/classic_games/games/snake/'
FOOD_SPEED = 1.5
FOOD_SPEED_TIME = 20