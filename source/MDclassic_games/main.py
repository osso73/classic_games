# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# std libraries

# non-std libraries
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.settings import SettingsWithSpinner
from kivy.utils import platform
from kivy.lang import Builder

# my app imports
from drawer import MyDrawer
from menu import Menu
from snake.screen import ScreenSnake
from ahorcado.screen import ScreenAhorcado
from buscaminas.screen import ScreenBuscaminas
from game_15puzzle.screen import Screen15Puzzle
from game_2048.screen import Screen2048
from memory.screen import ScreenMemory
from pong.screen import ScreenPong


__version__ = '0.1'


KV = r"""

Screen:

    MDNavigationLayout:

        ScreenManager:
            id: screen_manager
            
            Menu:
                id: menu

            ScreenSnake:
                id: snake

            ScreenAhorcado:
                id: ahorcado

            ScreenBuscaminas:
                id: buscaminas
            
            Screen15Puzzle:
                id: fifteen

            Screen2048:
                id: 2048

            ScreenMemory:
                id: memory
            
            ScreenPong:
                id: pong
            
        
        MyDrawer:
            id: my_drawer
            
            on_screen:
                screen_manager.current = self.screen

"""

class MainApp(MDApp):
    """Main app"""
    
    def build(self):
        screen = Builder.load_string(KV)
        self.icon = 'images/icon.png'
        self.theme_cls.primary_palette = 'DeepPurple'
        self.settings_cls = SettingsWithSpinner
        self.use_kivy_settings = False
        return screen       

    def build_config(self, config):
        config.setdefaults('Snake', {
            'speed': '1',
            'size': '11',
            'mode': '1',
            'level_start': 1,
            })

    def build_settings(self, settings):
        settings.add_json_panel("Snake settings",
                                self.config,
                                filename='snake/settings.json')



    def on_config_change(self, config, section, key, value):
        speeds = {'11':'1', '15':'1.5', '19':'2', '23':'3' }
        sizes = {v:k for k,v in speeds.items()}

        if key == 'speed':
            self.root.ids.snake.ids.game.speed_factor = float(value)

        elif key == 'size':
            self.root.ids.snake.ids.game.size_snake = int(value)
            self.root.ids.snake.ids.game.set_size()

        elif key == 'mode':
            self.root.ids.snake.ids.game.story = bool(int(value))

        elif key == 'level_start':
            num = int(value)
            if num < 1:
                num = 1
            elif num > 12:
                num = 12
            config.set('Snake', 'level_start', num)

        config.write()


if __name__ == '__main__':
    if platform != 'android':
        Window.size = (400, 750)
    
    MainApp().run()

