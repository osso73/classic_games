#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 10:11:34 2021

@author: oriol
"""

import os


IMAGES = os.path.join(os.path.dirname(__file__), 'images')  # path of images
DOUBLE_TAP = 0.3  # seconds to wait to evaluat if double-tap is clicked
LEVELS = {
    1: {'mines': 10, 'columnas': 9, 'filas': 9, 'window': (1,1)},
    2: {'mines': 25, 'columnas': 9, 'filas': 18, 'window': (1,2)},
    3: {'mines': 125, 'columnas': 18, 'filas': 36, 'window': (1,2)},    
    }
