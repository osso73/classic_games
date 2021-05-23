#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton, MDFloatingActionButton


class DemoApp(MDApp):
    
    def build(self):
        '''
        Color Options in primary_palette - Available options are: 
            'Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 
            'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 
            'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 
            'BlueGray'
        
        Primary hue option:
            '50', '100', '200', '300', '400', '500', '600', '700', '800', 
            '900', 'A100', 'A200', 'A400', 'A700'.
        
        theme_style - Dark or Light two options
        '''
        self.theme_cls.primary_palette = 'Yellow'
        self.theme_cls.primary_hue = 'A700'
        self.theme_cls.theme_style = 'Dark'
        screen = Screen()
        btn_flat = MDRectangleFlatButton(text='Hello World', 
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        screen.add_widget(btn_flat)     
   
        return screen
    
if __name__ == '__main__':
    DemoApp().run()