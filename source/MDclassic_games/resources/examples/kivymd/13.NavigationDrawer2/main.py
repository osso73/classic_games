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
                        elevation: 10
                        left_action_items: [["menu", lambda x: nav_drawer.toggle_nav_drawer()]]

                    Widget:
                    
        MDNavigationDrawer:
            id: nav_drawer
            BoxLayout:
                orientation: 'vertical'
                spacing: '8dp'
                padding: '8dp'
                Image:
                    source: 'picture.png'
                
                MDLabel:
                    text: '  Susana'
                    font_style: 'Subtitle1'
                    size_hint_y: None
                    height: self.texture_size[1]
                
                MDLabel:
                    text: '  pastor.librada@gmail.com'
                    font_style: 'Caption'
                    size_hint_y: None
                    height: self.texture_size[1]
                
                ScrollView:
                    MDList:
                        OneLineIconListItem:
                            text: 'Profile'
                            IconLeftWidget:
                                icon: 'face-profile'
                        OneLineIconListItem:
                            text: 'Upload'
                            IconLeftWidget:
                                icon: 'upload'
                        OneLineIconListItem:
                            text: 'Logout'
                            IconLeftWidget:
                                icon: 'logout'
                    
'''

class DemoApp(MDApp):
    
    def build(self):
        self.theme_cls.primary_palette = 'Teal'
        screen = Builder.load_string(navigation_helper)
        return screen
    

if __name__ == '__main__':
    DemoApp().run()
