#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 18:08:56 2020

@author: osso73
"""


from kivy.app import App
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from kivy.properties import (
    NumericProperty, StringProperty, ListProperty,
    ObjectProperty, BooleanProperty
)

from random import sample
from time import sleep
import os


TEMAS = os.path.join(os.path.dirname(__file__), 'images', 'temas')


#######################################################################
class Tapete(GridLayout):
    '''
    Main area of the game, where the tiles are distributed. This class has 
    the logic to turn tiles, shuffle, etc. The tiles are distributed in a 
    GridLayout.
    
    Attributes
    ----------
    columnas : NumericProperty
        Number of columns of the GridLayout. 
    current_cards : ListProperty
        Cards that are turned up, but not yet matched. This list can have 0, 1
        or 2 cards max.
    movimientos : NumericProperty
        Count the number of moves that have been made. It is the score.
    imagenes : list
        List of filenames of the images.
        
    '''
    columnas = NumericProperty(2)
    current_cards = ListProperty()
    movimientos = NumericProperty(0)
    
        
    def load_images(self, app):
        '''
        Load images of current theme, and return them.

        Parameters
        ----------
        app : App
            Instance of the running app.

        Returns
        -------
        ims : list
            List of filenames of the images. These are the images of the 
            current theme.
        back : string
            Filename of the image shown in the back of the cards.

        '''
        p = os.path.join(TEMAS, app.root.tema_actual) 
        ims = os.listdir(p)
        ims = [os.path.join(p,im) for im in ims if im.startswith('image')]
        back = os.path.join(p,'back.jpg')
        return ims, back
        
    def start_game(self):
        '''
        Start the game: reset score to 0, load images according to currently
        selected theme and size, and create the tiles.
        '''
        self.clear_widgets()
        
        app = App.get_running_app()
        num = app.root.tamano
        app.root.play('start')
        self.imagenes, back = self.load_images(app)
        self.movimientos = 0
        
        # take only a number of images of the total, duplicate and shuffle
        imagenes = sample(self.imagenes, num)
        imagenes = sample(imagenes*2, num*2)
        
        self.set_columns(num)     
        for im in imagenes:
            self.add_widget(Carta(image=im, back=back))
    
    def set_columns(self, num):
        '''
        Define the columns of the widget, how the tiles will be distributed
        based on the number of tiles. The thresholds are determined by trial
        and error, based on the shape factor of a mobile phone.

        Parameters
        ----------
        num : int
            Total number of pairs of images to be distributed.
        '''
        if num < 5:
            self.columnas = 2
        elif num < 10:
            self.columnas = 3
        elif num < 16:
            self.columnas = 4
        else:
            self.columnas = 5
        
    def on_current_cards(self, *args, **kwargs):
        '''
        When the list of current cards changes, check if the length of the
        list is 2; if so, check if the pair match, in which case the cards
        are left with the image; if no match, turn the cards down again.
        '''
        if len(self.current_cards) == 2:
            self.movimientos += 1
            if self.current_cards[0].image != self.current_cards[1].image:
                sleep(2)  # wait 2 seconds before turning back cards
                self.current_cards.pop().turn()
                self.current_cards.pop().turn()
            else:
                self.current_cards.pop()
                self.current_cards.pop()
                app = App.get_running_app()
                app.root.play('ok')
                self.check_end()  # check if the game is finished
    
    def check_end(self):
        '''
        Check if the game is finished: all cards are up.
        '''
        for carta in self.children:
            if not carta.shown:
                return
        
        app = App.get_running_app()
        app.root.play('end_game')
        p = Popup(title='Final', size_hint=(0.75, 0.15),
                  content=PopupMsg(text='!Muy bien!\nHas encontrado todas las parejas'))
        p.open()

        
#######################################################################
class Carta(Button):
    '''
    This class defines the behaviour of each card: the image that is in the 
    front and the back, and its status (shown or not shown). The card is 
    modeled as a button with an image, which can be the back of the card or
    the front. Action occurs when button is clicked.
    
    Attributes
    ----------
    back : StringProperty
        Filename of the image that appears as back of the card.
    image : StringProperty
        Filename of the image that is in the front of the card.
    show : StringProperty
        Filename of the image that is shown at each moment. It is one of the
        two: image or show.
    shown : BooleanProperty
        Whether the card is turned up or down. False == turned down.
    
    '''
    back = StringProperty()
    image = StringProperty()
    show = StringProperty()
    shown = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super(Carta, self).__init__(**kwargs)
        self.show = self.back

    def click(self):
        '''
        When button is clicked, trigger the function to turn the card.
        '''
        if not self.shown:
            self.turn()
            app = App.get_running_app()
            app.root.play('turn')
            Clock.schedule_once(self.add_card_to_current)
            
    def add_card_to_current(self, *args):
        '''
        Add card to Tapete.current_cards list.
        '''
        app = App.get_running_app()
        app.root.ids.obj_tapete.current_cards.append(self)
        
    def turn(self):
        '''
        Turn the card. If the card is shown, turns it back; if not, 
        turn it up.
        '''
        if self.shown:
            self.show = self.back
        else:
            self.show = self.image
        self.shown = not self.shown
        

#######################################################################
class MainScreen(BoxLayout):
    '''
    This class organizes the mainscreen in the different areas: menu at the 
    top, and the board with the cards for the rest of screen.
    
    Attributes
    ----------
    sounds : dict
        Dictionary of sounds, containing all sounds to be played during the 
        game. Different functions will play them as needed.
    tamano : NumericProperty
        Number of pairs to be discovered.
    tema_actual : StringProperty
        Current theme to be used.
    lista_temas : list
        List of themes available.
    '''
    tamano = NumericProperty(6)
    tema_actual = StringProperty()
    
    def __init__(self, **kwargs):
        '''
        Create the list of themes based on the folders available, load the
        sounds to memory so they can be played without delay.
        '''
        super(MainScreen, self).__init__(**kwargs)
        self.lista_temas = os.listdir(TEMAS)
        self.cambiar_tema()
        self.sounds = self.load_sounds()
        
    def cambiar_tema(self):
        '''
        Switch to the following theme of the lista_temas.
        '''
        if not self.tema_actual:
            self.tema_actual = self.lista_temas[0]
        else:
            ind = self.lista_temas.index(self.tema_actual)
            new_ind = ind+1 if ind<len(self.lista_temas)-1 else 0
            self.tema_actual = self.lista_temas[new_ind]
    
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
        for s in ['bye', 'ok', 'start', 'turn', 'end_game']:
            sound[s] = SoundLoader.load(os.path.join(folder, f'{s}.ogg'))
            
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
        if sound in self.sounds:
            self.sounds[sound].play()
        else:
            raise Exception("Bad sound")

    def bye(self):
        '''
        Play a sound before closing the app, and wait a delay so the sound 
        can be heard (Trump saying 'thank you very much')
        '''
        self.play('bye')
        sleep(1.5)



class PopupMsg(Label):
    pass

class MenuButton(Button):
    pass

class MenuButtonSmall(Button):
    pass

class MenuLabel(Label):
    pass



class MemoryApp(App):    
    def build(self):
        self.icon = os.path.join(os.path.dirname(__file__), 
                                 'images', 'icon.png')
        main = MainScreen()
        return main


if __name__ == '__main__':
    # Window.size = (1080, 2340)
    Window.size = (500, 1000)
    MemoryApp().run()
