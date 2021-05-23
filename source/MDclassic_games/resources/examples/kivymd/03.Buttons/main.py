#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton, MDFloatingActionButton


class DemoApp(MDApp):
    
    def build(self):
        screen = Screen()
        btn_flat = MDFlatButton(text='Hello World', 
                                pos_hint={'center_x': 0.5, 'center_y': 0.25})
        
        btn_rect_flat = MDRectangleFlatButton(text='Hello World', 
                                pos_hint={'center_x': 0.5, 'center_y': 0.75})
        
        icon_btn = MDIconButton(icon='android', 
                                pos_hint={'center_x': 0.25, 'center_y': 0.5})
        
        action_icon_btn = MDFloatingActionButton(icon='language-python', 
                                pos_hint={'center_x': 0.75, 'center_y': 0.5})
        
        screen.add_widget(btn_flat)     
        screen.add_widget(btn_rect_flat)     
        screen.add_widget(icon_btn)
        screen.add_widget(action_icon_btn)
   
        return screen
    
if __name__ == '__main__':
    DemoApp().run()