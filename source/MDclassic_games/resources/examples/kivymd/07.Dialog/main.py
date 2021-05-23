#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
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
        if self.username.text == "":
            check_string = 'Please enter a username'
        else:
            check_string = self.username.text
        
        close_btn = MDFlatButton(text='Close', on_release=self.close_dialog)
        more_btn = MDFlatButton(text='More...')
        self.dialog = MDDialog(text=check_string, title='Username check',
                          size_hint_x=0.75,
                          buttons=[close_btn, more_btn])
        self.dialog.open()
    
    
    def close_dialog(self, obj):
        self.dialog.dismiss()
        
    
    
if __name__ == '__main__':
    DemoApp().run()