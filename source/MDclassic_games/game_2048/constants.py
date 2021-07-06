#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 19:26:36 2021

@author: oriol
"""

import os


SPACING = 20
TILES = os.path.join(os.path.dirname(__file__), 'images', 'tiles')  # path of images
MOVE_TILE = 0.075
MOVE_DURATION = MOVE_TILE + 0.06
MINIMUM_SWIPE = 50
SCORES = [256, 512, 1024, 2048]
NEW_TILE_SEQUENCE = [2]*4 + [4]
URL_HELP = 'https://osso73.github.io/classic_games/games/classic_games/#game-of-2048'