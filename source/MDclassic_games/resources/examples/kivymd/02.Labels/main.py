#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel, MDIcon


class DemoApp(MDApp):
    def build(self):
        # using colours: https://raw.githubusercontent.com/HeaTTheatR/KivyMD-data/master/gallery/kivymddoc/md-label-theme-text-color.png
        # choose standard theme colour
        label = MDLabel(text='Hello world', halign='center', 
                        theme_text_color='Error')
        # choose custom colour
        label = MDLabel(text='Hello world', halign='center', 
                        theme_text_color='Custom', text_color=(236/255, 98/255, 81/255, 1))

        # using font styles https://github.com/HeaTTheatR/KivyMD/blob/master/kivymd/icon_definitions.py
        label = MDLabel(text='Hello world', halign='center', 
                        theme_text_color='Custom', text_color=(236/255, 98/255, 81/255, 1),
                        font_style='H1')
        
        # using icons 
        icon_label = MDIcon(icon='language-python', halign='center')
        
        

        # return label
        return icon_label
    
if __name__ == '__main__':
    DemoApp().run()