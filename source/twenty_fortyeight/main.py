#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 16:50:53 2020

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
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout

from kivy.properties import (
    NumericProperty, StringProperty, ListProperty,
    ObjectProperty, BooleanProperty
)

from time import sleep
from random import choice
from functools import partial

SPACING = 20
TILES = 'images/tiles/'
MOVE_TILE = 0.075
MOVE_DURATION = MOVE_TILE + 0.06
MINIMUM_SWIPE = 50
SCORES = [256, 512, 1024, 2048]
NEW_TILE_SEQUENCE = [2]*4 + [4]


class Tile(Label):
    '''
    Represents one of the tiles in the board.

    Attributes
    ----------
    value : int
        The number shown on the tile. For each value, a different image is
        shown, showing the value and a colour.
    position: list (i, j)
        Position of the tile in the grid. i, j can have values from 0 to 3
    tamano: int
        Size of the tile, in pixels. Needed to calculate position of tile in 
        screen
    merged: boolean
        Has this tile been merged? This is put to False when move start, and 
        becomes True in case of merging, to avoid a second merge in the 
        same move
    
    '''
    value = NumericProperty(0)
    position = ListProperty()
    tamano = NumericProperty()
    merged = False
    _previous = 0
    
    def calc_position(self):
        '''
        calculate position of Tile in screen, based on attribute self.position

        Returns
        -------
        (x, y) : tuple
            Coordinates in screen
        '''
        return (self.position[0]*(self.tamano) + SPACING, 
                (self.position[1])*(self.tamano) + SPACING)
    
    def on_position(self, *args):
        '''
        When position changes, trigger an animation to move to the new
        position on screen, and play sound of moving Tile.
        '''
        if self.value:  # don't move empty tiles (e.g. self.value=0)
            anim = Animation(pos=self.calc_position(), duration=MOVE_TILE)
            anim.start(self)
            app = App.get_running_app()
            app.root.play('move')

    
    def on_value(self, tile, value):
        '''
        When value attribute changes, trigger animation: if previous value
        is 0, animation to spawn a new Tile; if not, animation of merge.

        Use self._previous to store the previous value.
        '''
        x, y = self.size
        if self._previous != 0:
            anim = Animation(size=(1.1*x, 1.1*y), duration=0.05) + \
                Animation(size=(x, y), duration=0.05)
            anim.start(self)
            self.merged = True
            self.parent.score += value
        else:
            m,n = self.pos
            self.size = [0, 0]
            self.pos = [m+self.tamano/2, n+self.tamano/2]
            anim = Animation(size=(x, y), pos=(m, n), duration=0.1)
        anim.start(self)
        self._previous = self.value

    
class Board(RelativeLayout):
    '''
    Board containing the 16 tiles that are moved. This class contains all
    the intelligence of the moves, and checks if game is finished.

    Attributes
    ----------
    ventana : int
        Size of the board, in pixels.
    win_score : int
        Value of the tile that is required to win (2048 by default)
    score : int
        Current score. Score is the sum of all values of tiles that have
        merged.
    swipe_x, swipe_y : int
        Coordinates on the screen of initial position of swipe move
    active_game : boolean
        The game is active when it starts, until it finished (due to reaching
        the win_score or lack of possible moves)
    last_move: list
        Stores the position and value of all tiles before starting the move. 
        Used to enable go_back method.
    
    '''
    ventana = NumericProperty()
    win_score = NumericProperty(2048)
    score = NumericProperty(0)
    swipe_x = swipe_y = 0
    active_game = False
    last_move = ListProperty()
    _moving = False
    _moved_tile = False
    
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        Clock.schedule_once(self.initialize_grid)
    
    def initialize_grid(self, *args):
        '''
        initialisation is triggered after the parent window has been set up
        '''
        self.ventana = min(self.parent.height, self.parent.width)
        
    def on_touch_down(self, touch):
        '''
        When touch down, store the value of (x, y) in attributes swipe_x
        and swipe_y. These will be used by method on_touch_up.

        Parameters
        ----------
        touch : touch event
            contains the coordinates of the touch.
        '''
        if self.collide_point(touch.x, touch.y):
            self.swipe_x = touch.x
            self.swipe_y = touch.y
    
    def on_touch_up(self, touch):
        '''
        When touch up, compare coordinates with swipe_x, swipe_y to find
        the direction of the move, and trigger the move() method.

        Parameters
        ----------
        touch : touch event
            contains the coordinates of the touch.

        Returns
        -------
        direction : string
            Direction of the move.

        '''
        if self.collide_point(touch.x, touch.y):
            dif_x = self.swipe_x - touch.x
            dif_y = self.swipe_y - touch.y
            if abs(dif_x) > MINIMUM_SWIPE or abs(dif_y) > MINIMUM_SWIPE:
                if abs(dif_x) > abs(dif_y):
                    if dif_x > 0:
                        direction = 'left'
                    else:
                        direction = 'right'
                else:
                    if dif_y > 0:
                        direction = 'down'
                    else:
                        direction = 'up'
                self.move(direction)
                return direction

    def change_win_score(self):
        '''
        Change the winning score, cycling through values stored in SCORES
        global list. Store the new value in self.win_score.
        '''
        scores = SCORES
        ind = scores.index(self.win_score)
        new_ind = (ind + 1) % len(scores)
        self.win_score = scores[new_ind]
        
    def start_game(self):
        '''
        Start the game: resets the scores, rebuild the board, and add
        two new tiles.
        '''
        self.clear_widgets()
        self.active_game = True
        self.score = 0
        tamano = (self.ventana - SPACING) / 4
        for i in range(4):
            for j in range(4):
                self.add_widget(Tile(position=(i, j), tamano=tamano))        
        self.add_tile()
        self.add_tile()
        

    def add_tile(self, *args):
        '''
        Add a new tile on the board, i.e. change value attribute from 0 to a
        value. Value taken from a list of 2s and 4s.
        '''
        new_tile = choice(self.get_empty_tiles())
        new_tile.value = choice(NEW_TILE_SEQUENCE)
        
    def get_empty_tiles(self):
        '''
        Find all empty tiles (i.e. value==0) of the board.

        Returns
        -------
        list : list
            List of empty tiles.
        '''
        return [child for child in self.children if not child.value]


    def get_full_tiles(self, row=-1, col=-1):
        '''
        Return a list of tiles that are empty. If row or column are 
        specified, return only that row/column.

        Returns
        -------
        full_tiles : list
            List of non-empty tiles.
        '''
        full_tiles = [child for child in self.children if child.value]
        if row != -1:
            full_tiles = [t for t in full_tiles if t.position[0] == row]
        elif col != -1:
            full_tiles = [t for t in full_tiles if t.position[1] == col]
        
        return full_tiles
    
    def move(self, direction, *args):
        '''
        Trigger move of the tiles in a certain direction. Based on the
        direction will select the rows or columns that need to move, and
        trigger the moves squentially, leaving enough time in between for 
        the move to finish before the next row/column moves.

        Parameters
        ----------
        direction : string
            Direction of the move. Can be 'up', 'down', 'left' or 'right'.
        
        '''
        if not self.active_game:
            return
        
        # if the previous move still ongoing, wait (re-schedule for later)
        if self._moving:
            Clock.schedule_once(partial(self.move, direction), 0.01)
        else:
            self._moving = True
            self._moved_tile = False
            self.save_last_move()
            if direction == 'right':
                for n, row in enumerate([2, 1, 0]):
                    Clock.schedule_once(partial(self.move_row_line, 
                                                direction, 
                                                self.get_full_tiles(row=row)),
                                        MOVE_DURATION*n)
            elif direction == 'left':
                for n, row in enumerate([1, 2, 3]):
                    Clock.schedule_once(partial(self.move_row_line, 
                                                direction, 
                                                self.get_full_tiles(row=row)),
                                        MOVE_DURATION*n)
            elif direction == 'up':
                for n, col in enumerate([2, 1, 0]):
                    Clock.schedule_once(partial(self.move_row_line, 
                                                direction, 
                                                self.get_full_tiles(col=col)),
                                        MOVE_DURATION*n)
            else:
                for n, col in enumerate([1, 2, 3]):
                    Clock.schedule_once(partial(self.move_row_line, 
                                                direction, 
                                                self.get_full_tiles(col=col)),
                                        MOVE_DURATION*n)
            Clock.schedule_once(self.end_of_move, MOVE_DURATION*3)
    
    def end_of_move(self, *args):
        if self._moved_tile:
            self.add_tile()
            for child in self.children:
                child.merged = False
            self.end_of_game()
        self._moving = False
    
    def end_of_game(self):
        app = App.get_running_app()
        if [child for child in self.children if child.value >= self.win_score]:
            # win game
            msg = 'Has ganado!'
            app.root.play('end_win')
        
        elif not self.available_moves():
            # no empty tiles --> lose game
            msg = 'Has perdido\nYa no puedes mover!'
            app.root.play('end_lose')
        
        else:
            return
        
        p = Popup(title='Final', size_hint=(0.75, 0.20),
                  content=Message(text=msg))
        p.open()
        self.active_game = False
    
    def available_moves(self):
        for tile in self.children:
            if not tile.value:
                return True
            i, j = tile.position
            for p in [[i+1, j], [i-1, j], [i, j+1], [i, j-1]]:
                t = self.get_tile(p)
                if t and tile.value == t.value:
                    return True
        return False

                
        
    def move_row_line(self, direction, row_line, *args):
        for tile in row_line:
            self.move_tile(direction, tile)
    
    def move_tile(self, direction, tile):
        old_position = tile.position
        final_position = self.check_final(direction, old_position, tile.value)
        if final_position != old_position:
            self.add_widget(Tile(position=old_position, tamano=tile.tamano))        
            self.remove_widget(tile)
            self.add_widget(tile)  # to ensure it in on top
            tile_to_remove = self.get_tile(final_position)
            tile.position = final_position
            Clock.schedule_once(partial(self.end_of_move_tile, tile_to_remove, tile), 
                                MOVE_TILE)
    
    def end_of_move_tile(self, tile_to_remove, tile, *args):
        tile.value += tile_to_remove.value
        self.remove_widget(tile_to_remove)
        self._moved_tile = True
        
    def check_final(self, direction, position, value):
        x, y = position
        if direction == 'left':
            x -= 1
        elif direction == 'right':
            x += 1
        elif direction == 'up':
            y += 1
        else:
            y -= 1
        if (x not in range(4)) or (y not in range(4)):
            return position
        new_position = [x, y]
        new_tile = self.get_tile(new_position)
        if not new_tile:
            raise Exception("tile not found!!")
        if new_tile.value:
            if new_tile.value == value and not new_tile.merged:
                return new_position
            else:
                return position
        return self.check_final(direction, new_position, value)
        
    def get_tile(self, position):
        for child in self.children:
            if child.position == position:
                return child

    def save_last_move(self):
        self.last_move = []
        for child in self.children:
            tile = dict()
            tile['value'] = child.value
            tile['position'] = child.position
            tile['tamano'] = child.tamano
            tile['score'] = self.score
            self.last_move.append(tile)            
            

    def back_button(self):
        if self.active_game:
            self.clear_widgets()
            for tile in self.last_move:
                obj = Tile(position=tile['position'], tamano=tile['tamano'])
                self.add_widget(obj)
                obj.value = tile['value']
                self.score -= tile['value']
            self.score = tile['score']
            


############################# ButtonJoystick #################################
class ButtonJoystick(Button):
    icon = StringProperty()

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.sounds = self.load_sounds()
        
    def cambiar_tema(self):
        if not self.tema_actual:
            self.tema_actual = self.lista_temas[0]
        else:
            ind = self.lista_temas.index(self.tema_actual)
            new_ind = ind+1 if ind<len(self.lista_temas)-1 else 0
            self.tema_actual = self.lista_temas[new_ind]
    
    def load_sounds(self):
        sound = dict()
        sound['bye'] = SoundLoader.load('audio/bye.ogg')
        sound['start'] = SoundLoader.load('audio/start.ogg')
        sound['move'] = SoundLoader.load('audio/move.ogg')
        sound['end_win'] = SoundLoader.load('audio/end_win.ogg')
        sound['end_lose'] = SoundLoader.load('audio/end_lose.ogg')
        
        return sound
    
    def play(self, sound):
        if sound in self.sounds:
            self.sounds[sound].play()
        else:
            raise Exception("Bad sound")

    def bye(self):
        self.play('bye')
        sleep(1.5)


class Message(Label):
    pass

class NewButton(Button):
    pass


class PuzzleApp(App):    
    def build(self):
        self.icon = 'images/icon.png'
        main = MainScreen()
        return main


if __name__ == '__main__':
    # Window.size = (1080, 2340)
    Window.size = (375, 800)
    PuzzleApp().run()

