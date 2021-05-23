#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

Window.size = (300, 500)

screen_helper = '''
Screen:
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'Demo'
            left_action_items: [["menu", app.navigation_draw]]
            right_action_items: [["clock", app.navigation_draw]]
            elevation: 10
        MDLabel:
            text: 'Hello World'
            halign: 'center'
        
        MDBottomAppBar:
            MDToolbar:
                title: 'Help'
                left_action_items: [["coffee", app.navigation_draw]]
                mode: 'end'
                type: 'bottom'
                on_action_button: app.navigation_draw()
                icon: 'language-python'
                
'''

class DemoApp(MDApp):
    
    def build(self):
        self.theme_cls.primary_palette = 'Purple'
        screen = Builder.load_string(screen_helper)
        return screen
    
    def navigation_draw(self, *args):
        print("Navigation", args)
        


if __name__ == '__main__':
    DemoApp().run()
