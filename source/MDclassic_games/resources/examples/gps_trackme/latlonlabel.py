#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 20:27:01 2021

@author: oriol
"""


# std libraries

# non-std libraries
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder

# my app imports
from constants import *



Builder.load_string(
    r'''

<LatLonLabel>:
    text: "Lat: " + self.lat_label + "\nLon: " + self.lon_label
    size_hint_y: None
    height: self.texture_size[1]
    halign: 'center'
    font_style: 'H5'
    padding: 0, '15dp'

''')



class LatLonLabel(MDLabel):
    lat = NumericProperty(SEARCHING_GPS_NUM)
    lon = NumericProperty(SEARCHING_GPS_NUM)
    lat_label = StringProperty(SEARCHING_GPS_TEXT)
    lon_label = StringProperty(SEARCHING_GPS_TEXT)
    fmt = 'dms'


    def on_lat(self, *args):
        self.lat_label = self.get_coordinate('lat')
    

    def on_lon(self, *args):
        self.lon_label = self.get_coordinate('lon')
    

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.fmt = 'deg' if self.fmt == 'dms' else 'dms'
            self.lat_label = self.get_coordinate('lat')
            self.lon_label = self.get_coordinate('lon')
            return True
    
    

    def get_coordinate(self, coord_type):
        coord = self.lat if coord_type == 'lat' else self.lon

        if coord == NO_GPS_NUM:
            return NO_GPS_TEXT
        
        if coord == SEARCHING_GPS_NUM:
            return SEARCHING_GPS_TEXT
        
        if self.fmt == 'deg':
            return f'{coord:0.5f}'
        
        else:    # transform to other coordinates
            if coord_type == 'lat':
                letter = 'S' if coord < 0 else 'N'
            else:
                letter = 'W' if coord < 0 else 'E'

            coord = abs(coord)
            d = int(coord)
            rest = (coord - d) * 60
            m = int(rest)
            s = (rest - m) * 60
            
            return f'{letter} {d}º {m}\' {s:.2f}"'
            
    