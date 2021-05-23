#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from navigation import screen_helper

Window.size = (300, 500)



class ProfileScreen(Screen):
    pass


class MenuScreen(Screen):
    pass


class UploadScreen(Screen):
    pass



class DemoApp(MDApp):
    
    def build(self):
        self.theme_cls.primary_palette = 'DeepOrange'
        screen = Builder.load_string(screen_helper)

        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(ProfileScreen(name='profile'))
        sm.add_widget(UploadScreen(name='upload'))


        return screen
    

if __name__ == '__main__':
    DemoApp().run()
