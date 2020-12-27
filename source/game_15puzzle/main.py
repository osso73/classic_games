#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 19:00:00 2020

@author: osso73
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.animation import Animation

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout

from kivy.properties import (
    NumericProperty, StringProperty, ListProperty,
    ObjectProperty, BooleanProperty
)

from time import sleep
from random import shuffle
import os
import math


SPACING = 10  # spacing between tiles (in pixels)
MOVE_DURATION = 0.1  # duration of the move
TEMAS = 'images/temas'  # folder of the themes

class Puzzle(RelativeLayout):
    '''
    This is the widget that holds the logic of the game. Tiles are organized
    through a RelativeLayout so that animation can be used when moving tiles.
    The Tiles are children to this widget, including the empty space.
    
    Attributes
    ----------
    ventana : NumericProperty
        Width and height of the widget. Determined from parent's size.        
    movimientos : NumericProperty
        Count the number of moves made (for the score).
    tamano : NumericProperty
        Size of the board: 3 for 3x3, 4 for 4x4, 5 for 5x5
        
    '''
    ventana = NumericProperty(100)
    movimientos = NumericProperty(0)
    tamano = NumericProperty(3)
    
    def __init__(self, **kwargs):
        super(Puzzle, self).__init__(**kwargs)
        # launch initialize in the next iteration, once the main window is
        # defined, to ensure it has height and width
        Clock.schedule_once(self.initialize_grid)
    
    def initialize_grid(self, *args):
        '''
        Establish the width and height of the widget, based on parent's size
        '''
        self.ventana = min(self.parent.height, self.parent.width)
    
    def start_game(self):
        '''
        Start a new game: play sound of start, build the tiles, reset score.
        '''
        self.parent.play('start')
        self.clear_widgets()
        app = App.get_running_app()
        self.tamano = app.root.ids.muestra.tamano
        self.movimientos = 0
        
        # create list of tiles. Each tile has a number, so its order can be
        # checked. A blank tile is added at the end
        lado = int(self.ventana / self.tamano)
        title = list(range(1, self.tamano**2)) + ['']
        shuffle(title)
        
        # ensure that the puzzle is solvable; if not shuffle again
        while not self.is_solvable(title):
            shuffle(title)
        
        # create tiles as widgets added to the Puzzle
        n = 0
        for i in range(self.tamano):
            for j in range(self.tamano):
                self.add_widget(Ficha(name=str(title[n]), lado=lado, 
                                      tamano=self.tamano,
                                      size=(lado-SPACING, lado-SPACING),
                                      size_hint=(None, None), posicion=(j, i)))
                n += 1
        # load theme
        self.parent.ids.muestra.load_tema()

    def find_empty(self):
        '''
        Find the empty tile in the board.

        Returns
        -------
        Tile
            The tile that is empty. If no empty tile found, return False.

        '''
        for child in self.children:
            if not child.name:
                return child       
        return False

    def check_win(self):
        '''
        Check if game has finished: all tiles should be in order.

        Returns
        -------
        bool
            True if the game has finished, False if not.

        '''
        for child in self.children:
            if not child.name:
                continue
            if int(child.name) != (child.posicion[0] + 
                                   child.posicion[1] * self.tamano + 1):
                return False        
        return True
    
    def end_of_game(self):
        '''
        Check if the picture is complete. If so, convert empty tile to the 
        last piece of the puzzle, and show it with an animation
        '''
        if self.check_win():
            self.parent.play('end_game')
            lado = int(self.ventana / self.tamano)
            for child in self.children:
                if not child.name:
                    child.name=str(self.tamano**2)
                    child.size=(0,0)
                
                # animation is applied to all tiles
                anim = Animation(size=(lado, lado), duration=0.5)
                anim.start(child)
                

    
    def is_solvable(self, game):
        '''
        Check if the game provided is solvable or not. Based on the algorithm
        explained here: 
        https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/

        Parameters
        ----------
        game : list
            Values of the game in the order they are shown. The blank tile 
            should be represented by ''. The values can be int or 
            strings, they are converted to int.

        Raises
        ------
        Exception
            If the game is not square.
        ValueError
            If the blank piece not in the list. It has to be ''.

        Returns
        -------
        bool
            True if the game is solvable; False if not.

        '''
        lado = math.sqrt(len(game))
        if int(lado) != lado:
            raise Exception('Game sequence not an exact square.')
        
        if '' not in game:
            raise ValueError("Blank tile missing. Expected ''")
        
        lado = int(lado)
        seq = [int(n) for n in game if n]
        inversions = 0
        for n in seq:
            for m in seq:
                if seq.index(n) < seq.index(m) and n > m:
                    inversions += 1
        
        if lado % 2:
            if inversions % 2:
                return False
            else:
                return True
        else:
            blank = game.index('')
            row_blank = lado - blank // lado
            if row_blank % 2:
                if not inversions % 2:
                    return True
                else:
                    return False
            else:
                if inversions % 2:
                    return True
                else:
                    return False


class Muestra(GridLayout):
    '''
    Control the bottom part of screen, showing the complete picture, so it 
    can be used as a reference. The picture is divided in tiles as well, to
    show the image of each tile.
    
    Use a GridLa
    Attributes
    ----------
    tema : StringProperty
        This controls what picture to show.
    tamano : NumericProperty
        Size of the board: 3 for 3x3, 4 for 4x4, 5 for 5x5
    ventana : float
        Width and height of the widget. Determined from parent's size.        
    '''
    tema = StringProperty('numeros')
    tamano = NumericProperty(3)
    
    def __init__(self, **kwargs):
        super(Muestra, self).__init__(**kwargs)
        Clock.schedule_once(self.load_tema)
    
    def initialize_grid(self, *args):
        '''
        Establish the width and height of the widget, based on parent's size
        '''
        self.ventana = min(self.parent.height, self.parent.width)

    def load_tema(self, *args):
        '''
        Load a new picture to be used, and divides it into the tiles as 
        defined by self.tamano. Load all tiles.
        '''
        self.initialize_grid()
        self.clear_widgets()
        self.cols = self.tamano
        for n in list(range(1, self.tamano**2 + 1)):
            self.add_widget(FichaMuestra(name=str(n)))

    def cambiar_tema(self):
        '''
        Change the theme, used to load the picture. This is not changing the 
        picture, just the name. The picture is changed by method 
        load_tema().

        '''
        fullname = os.path.join(os.path.dirname(__file__), TEMAS)
        temas = os.listdir(fullname)
        ind = temas.index(self.tema)
        new_ind = (ind + 1) % len(temas)
        self.tema = temas[new_ind]
    
    def cambiar_tamano(self):
        '''
        Change the size of the board, cycling between 3x3, 4x4 and 5x5. 
        This is stored in variable self.tamano.
        '''
        nivel = self.tamano - 2
        nivel = nivel % 3 + 1
        self.tamano = nivel + 2

    
    def on_tema(self, *args):
        self.load_tema()
    
    def on_tamano(self, *args):
        self.load_tema()
                            

class Ficha(Label):
    '''
    Contains the properties and logic of the tiles and their movement.
    
    Attributes
    ----------    
    name : StringProperty
        Name of the tile, a number between 1 and the size of board -1.
    tamano : NumericProperty
        Size of the board: 3 for 3x3, 4 for 4x4, 5 for 5x5.
    lado : NumericProperty
        Length of the side, in pixels. Tiles are square.
    posicion : ListProperty
        Position in the board, starting from (0,0) at top-left, to (n,n) 
        bottom-right, n being the size of the board.
    filename : StringProperty
        Filename of the image to be shown.
    '''
    
    name = StringProperty()
    tamano = NumericProperty()
    lado = NumericProperty()
    posicion = ListProperty()
    filename = StringProperty()
    
    def __init__(self, **kwargs):
        super(Ficha, self).__init__(**kwargs)
        self.pos = self.calcular_posicion()
        app = App.get_running_app()
        tema = app.root.ids.muestra.tema
        tamano = app.root.ids.muestra.tamano
        if self.name:
            self.filename = f'images/temas/{tema}/{tamano}/{self.name}.jpg'
        else:
            self.filename = f'images/temas/{tema}/{tamano}/{tamano**2}.jpg'
    
    def calcular_posicion(self):
        '''
        Calculate the position on the canvas, in pixels, based on the posicion 
        attribute of the tile

        Returns
        -------
        tuple
            Coordinates (x, y ) of the position on the canvas.
        '''
        return (self.posicion[0]*self.lado + SPACING/2, 
                (self.tamano-1-self.posicion[1])*self.lado + SPACING/2)
    
    def on_touch_down(self, touch):
        '''
        When tile is touched, it initiates the move to the empty space.

        Parameters
        ----------
        touch : touch event
            Position of the touch in screen.
        '''
        if self.collide_point(*touch.pos):
            self.move()
    
    def move(self):
        '''
        Move the tile if it is adjacent to empty space.
        '''
        empty = self.parent.find_empty()
        if empty:
            ex, ey = empty.posicion
            px, py = self.posicion
            if (ex==px and ey==py+1) or (ex==px and ey==py-1) or\
                (ey==py and ex==px+1) or (ey==py and ex==px-1):
                    empty.posicion, self.posicion = self.posicion, empty.posicion
                    self.parent.parent.play('move')
                    self.parent.movimientos += 1
            self.parent.end_of_game()
    
    def on_posicion(self, *args):
        '''
        When posicion changes, initiate the Animation of the move to the new
        position.
        '''
        anim = Animation(pos=self.calcular_posicion(), duration=MOVE_DURATION)
        anim.start(self)

                    
class FichaMuestra(Label):
    name = StringProperty()


class MenuButton(Button):
    pass

class MenuButtonSmall(Button):
    pass

class MenuLabel(Label):
    pass


class MainScreen(BoxLayout):    
    '''
    This class organizes the mainscreen in the different areas: menu at the 
    top, the main board in the middle, additional buttons in the middel, and 
    the reference picture at the bottom.
    
    Attributes
    ----------
    sounds : dict
        Dictionary of sounds, containing all sounds to be played during the 
        game. Different functions will play them as needed.
    '''
    def __init__(self, **kwargs):
        '''
        It triggers loading of sounds to memory when the game is launched, so
        they can be played without delay.
        '''
        super(MainScreen, self).__init__(**kwargs)
        self.sounds = self.load_sounds()

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
        for s in ['bye', 'ok', 'start', 'move', 'end_game']:
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
    


class PuzzleApp(App):    
    def build(self):
        self.icon = 'images/icon.png'
        main = MainScreen()
        return main


if __name__ == '__main__':
    # Window.size = (1080, 2340)
    Window.size = (375, 800)
    PuzzleApp().run()

