# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# std libraries
import os
import sys

# non-std libraries
from kivy.config import Config
from kivy.utils import platform

from android_insets import hide_system_bars, system_bar_insets
from audio_env import configure_audio_environment

# Kivy's bundled SDL mixer deadlocks through this host's PulseAudio bridge, so
# Linux desktops use ALSA. Android also reports sys.platform as 'linux' but only
# exposes its native audio backend, so its SDL audio driver is left untouched.
configure_audio_environment(platform)

# Reserve right-click for Buscaminas flags instead of Kivy's red multitouch markers.
if sys.platform.startswith('linux') and platform != 'android':
    Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.settings import SettingsWithSpinner
from kivy.lang import Builder
from kivy.clock import Clock

from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

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



__version__ = '1.2'


KV = r"""

# Preserve the classic DeepPurple toolbar across the menu and every game.
<MDTopAppBar>:
    theme_bg_color: "Custom"
    md_bg_color: "#673AB7"

<MDTopAppBarTitle>:
    theme_text_color: "Custom"
    text_color: "#FFFFFF"

<MDActionTopAppBarButton>:
    theme_icon_color: "Custom"
    icon_color: "#FFFFFF"

<MDChip>:
    theme_bg_color: "Custom"
    md_bg_color: "#673AB7"

<MDChipText>:
    theme_text_color: "Custom"
    text_color: "#FFFFFF"

<MDButton>:
    theme_bg_color: "Custom"
    md_bg_color: "#673AB7"

<MDButtonText>:
    theme_text_color: "Custom"
    text_color: "#FFFFFF"

<MDButtonIcon>:
    theme_icon_color: "Custom"
    icon_color: "#FFFFFF"

Screen:

    # Android 15+ forces edge-to-edge drawing, so insets are applied here to
    # keep the toolbar and content clear of the status and navigation bars.
    BoxLayout:
        id: content
        orientation: 'vertical'

        MDNavigationLayout:

            ScreenManager:
                id: screen_manager

                Menu:
                    id: menu

            MyDrawer:
                id: my_drawer

                on_screen: app.change_screen(self.screen)
                    

<TempMsg>:
    size_hint_x: 0.5
    pos_hint: {"center_x": .5, "bottom": 1}


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
        self.sounds = {}
        screen = Builder.load_string(KV)
        self.icon = 'images/icon.png'
        self.theme_cls.primary_palette = '#673AB7'
        self.settings_cls = SettingsWithSpinner
        self.use_kivy_settings = False
        return screen
    
    
    def on_start(self):
        self.sm = self.root.ids.screen_manager
        hide_system_bars(platform)
        Clock.schedule_once(self.apply_system_bar_insets, 0.5)
        Clock.schedule_once(self.load_sounds)
        

    def apply_system_bar_insets(self, *args):
        top, bottom = system_bar_insets(platform)
        self.root.ids.content.padding = [0, top, 0, bottom]


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
            if not self.sm.has_screen('snake'):
                self.sm.add_widget(ScreenSnake())
            self.sm.get_screen('snake').config_change(config, section, key, value)
        
        elif section == 'Ahorcado':
            if not self.sm.has_screen('ahorcado'):
                self.sm.add_widget(ScreenAhorcado())
            self.sm.get_screen('ahorcado').config_change(config, section, key, value)
        
        elif section == 'fifteen':
            if not self.sm.has_screen('fifteen'):
                self.sm.add_widget(Screen15Puzzle())
            self.sm.get_screen('fifteen').config_change(config, section, key, value)
        
        elif section == 'Memory':
            if not self.sm.has_screen('memory'):
                self.sm.add_widget(ScreenMemory())
            self.sm.get_screen('memory').config_change(config, section, key, value)
        
        elif section == 'Pong':
            if not self.sm.has_screen('pong'):
                self.sm.add_widget(ScreenPong())
            self.sm.get_screen('pong').config_change(config, section, key, value)
        

    def load_sounds(self, *args):
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

        self.sounds = sound
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
        
    
    def change_screen(self, new_screen):
        
        if not self.sm.has_screen(new_screen):
            if new_screen == 'pong':
                TempMsg(text='Loading pong...').open()
                self.sm.add_widget(ScreenPong())
            elif new_screen == 'ahorcado':
                TempMsg(text='Loading ahorcado...').open()
                self.sm.add_widget(ScreenAhorcado())
            elif new_screen == 'memory':
                TempMsg(text='Loading memory...').open()
                self.sm.add_widget(ScreenMemory())
            elif new_screen == 'fifteen':
                TempMsg(text='Loading 15 puzzle...').open()
                self.sm.add_widget(Screen15Puzzle())
            elif new_screen == '2048':
                TempMsg(text='Loading 2048...').open()
                self.sm.add_widget(Screen2048())
            elif new_screen == 'buscaminas':
                TempMsg(text='Loading buscaminas...').open()
                self.sm.add_widget(ScreenBuscaminas())
            elif new_screen == 'snake':
                TempMsg(text='Loading snake...').open()
                self.sm.add_widget(ScreenSnake())
        
        self.sm.current = new_screen


class TempMsg(MDSnackbar):
    def init_fbos(self):
        # Loading messages have no interactive ripple, avoiding KivyMD's invalid FBO.
        pass

    def __init__(self, text, **kwargs):
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', 48)
        super().__init__(MDSnackbarText(text=text), **kwargs)


if __name__ == '__main__':
    if platform != 'android':
        Window.size = (400, 750)
    
    MainApp().run()
