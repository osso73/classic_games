#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  2 17:51:41 2021

@author: oriol
"""

# std libraries

# non-std libraries
from kivy_garden.mapview import MapView
from kivy.properties import BooleanProperty
from kivy.lang import Builder

# my app imports
from gpsblinker import GpsBlinker



Builder.load_string(
    r'''

<Map>:
    lat: 40.41806663677671
    lon: -3.703718024611724
    zoom: 10
    double_tap_zoom: True
    GpsBlinker:
        id: blinker
    
    
    MDIconButton:
        icon: 'crosshairs-gps' if root.center_map else 'crosshairs'
        on_release: root.center_map = not root.center_map

''')


class Map(MapView):
    center_map = BooleanProperty(True)
