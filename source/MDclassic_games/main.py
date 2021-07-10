# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# std libraries
import os


# non-std libraries
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
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



__version__ = '1.1'


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
    """
    Main app
    
    Parameters
    ----------
    sounds: list
        Dictionary of sounds to be played. Loaded at the init time, and used
        with the play() method throughout the program.
    
    """


    version = __version__
    
    def build(self):
        screen = Builder.load_string(KV)
        self.icon = 'images/icon.png'
        self.theme_cls.primary_palette = 'DeepPurple'
        self.settings_cls = SettingsWithSpinner
        self.use_kivy_settings = False
        return screen
    
    
    def on_start(self):
        self.sounds = self.load_sounds()
        

    def build_config(self, config):
        config.setdefaults('Pong', {
            'speed': 10,
            'max-speed': 50,
            'skin': 'original',
            })

        config.setdefaults('Ahorcado', {
            'man': 'man1',
            'keyboard': 'keyboard2',
            })

        config.setdefaults('Memory', {
            'level': 6,
            'theme': 'starwars',
            })

        config.setdefaults('fifteen', {
            'level': '1',
            'theme': 'numbers',
            })

        config.setdefaults('Snake', {
            'speed': '1',
            'size': '11',
            'mode': '1',
            'level_start': 1,
            })


    def build_settings(self, settings):
        settings.add_json_panel("Pong", self.config,
                                filename='pong/settings.json')
        settings.add_json_panel("Ahorcado", self.config,
                                filename='ahorcado/settings.json')
        settings.add_json_panel("Memory", self.config,
                                filename='memory/settings.json')
        settings.add_json_panel("15 puzzle", self.config,
                                filename='game_15puzzle/settings.json')
        settings.add_json_panel("Snake", self.config,
                                filename='snake/settings.json')


    def on_config_change(self, config, section, key, value):

        if section == 'Snake':
            self.root.ids.snake.config_change(config, section, key, value)
        
        elif section == 'Ahorcado':
            self.root.ids.ahorcado.config_change(config, section, key, value)
        
        elif section == 'fifteen':
            self.root.ids.fifteen.config_change(config, section, key, value)
        
        elif section == 'Memory':
            self.root.ids.memory.config_change(config, section, key, value)
        
        elif section == 'Pong':
            self.root.ids.pong.config_change(config, section, key, value)
        

    def load_sounds(self):
        '''
        Load all sounds of the game, and put them into the dictionary.

        Returns
        -------
        sound : dict
            The dictionary of sounds that have been loaded
        '''
        sound = dict()
        folder = os.path.join(os.path.dirname(__file__),'audio')
        soundlist = os.listdir(folder)
        for s in soundlist:
            sound[s] = SoundLoader.load(os.path.join(folder, s))

        return sound


    def play(self, sound):
        '''
        Play a sound from the dictionary of sounds.

        Parameters
        ----------
        sound : string
            Key of the dictionary corresponding to the sound to be played.

        Raises
        ------
        Exception
            If string passed is not in the dictionary.
        '''
        sound_name = sound + '.ogg'
        
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            raise Exception("Bad sound")



if __name__ == '__main__':
    if platform != 'android':
        Window.size = (400, 750)
    
    MainApp().run()

