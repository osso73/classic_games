#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window

Window.size = (300, 500)

navigation_helper = '''
Screen:
    NavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    MDToolbar:
                        title: 'Demo'
                        left_action_items: [["menu", lambda x: nav_drawer.toggle_nav_drawer()]]
                        elevation: 10
                    Widget:
        MDNavigationDrawer:
            id: nav_drawer
'''

class DemoApp(MDApp):
    
    def build(self):
        self.theme_cls.primary_palette = 'Orange'
        screen = Builder.load_string(navigation_helper)
        return screen
    

if __name__ == '__main__':
    DemoApp().run()
