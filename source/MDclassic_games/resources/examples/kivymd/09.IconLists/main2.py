#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Same functionality using kv language

"""

from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.list import OneLineListItem

screen_helper = '''
Screen:
    ScrollView:
        MDList:
            id: container
'''


class DemoApp(MDApp):

    def build(self):
        screen = Builder.load_string(screen_helper)
        return screen
    
    def on_start(self):
        '''
        This is automatically called for all KivyMD apps
        '''
        
        for n in range(20):
            items = OneLineListItem(text='Item ' + str(n))
            self.root.ids.container.add_widget(items)
   
    
if __name__ == '__main__':
    DemoApp().run()