#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder
from helpers import username_helper



class DemoApp(MDApp):
    
    def build(self):
        self.theme_cls.primary_palette = 'Red'
        screen = Screen()
        button = MDRectangleFlatButton(text='Show', on_release=self.show_data,
                                       pos_hint={'center_x': 0.5, 'center_y': 0.4})
        self.username = Builder.load_string(username_helper)
 
        screen.add_widget(self.username)
        screen.add_widget(button)
        return screen


    def show_data(self, obj):
        print(obj)
        print(self.username.text)
    
    
if __name__ == '__main__':
    DemoApp().run()