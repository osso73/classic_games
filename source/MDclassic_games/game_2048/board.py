#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 19:37:19 2021

@author: oriol
"""


# std libraries
from random import choice
from functools import partial
import os

# non-std libraries
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, ListProperty
from kivy.core.audio import SoundLoader

# my app imports
import game_2048.constants as G2048
from game_2048.tile import Tile
from game_2048.popup import PopupButton2048



Builder.load_string(
    r"""

<Board>:
    size: self.ventana, self.ventana
    size_hint: None, None
    canvas:
        Color:
            rgba: 0.55, 0.5, 0.5, 1
        Rectangle:
            pos: 0,0
            size: self.size
   
""")


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
    sounds: list
        Dictionary of sounds to be played. Loaded at the init time, and used
        with the play() method throughout the program.
    mute: boolean
        Controls if sounds should play or not. If True, sounds don't play.
    
    '''
    ventana = NumericProperty()
    win_score = NumericProperty(2048)
    score = NumericProperty(0)
    swipe_x = swipe_y = 0
    active_game = False
    last_move = ListProperty()
    mute = False
    _moving = False
    _moved_tile = False

    
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.sounds = self.load_sounds()


    def load_sounds(self):
        '''
        Load sounds in memory at the sstart of the program, so they can be
        played without delay.
        '''
        sound = dict()
        # sound['move'] = SoundLoader.load('audio/move.ogg')
        # sound['end_win'] = SoundLoader.load('audio/end_win.ogg')
        # sound['end_lose'] = SoundLoader.load('audio/end_lose.ogg')

        folder = os.path.join(os.path.dirname(__file__),'audio')
        for s in ['move', 'end_win', 'end_lose']:
            sound[s] = SoundLoader.load(os.path.join(folder, f'{s}.ogg'))

        return sound

    
    def play(self, sound):
        '''
        Function to play one of the sounds. It can be called from anywhere
        in the program.
        '''
        if self.mute:
            return
        
        if sound in self.sounds:
            self.sounds[sound].play()
        else:
            raise Exception("Bad sound")


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
            if abs(dif_x) > G2048.MINIMUM_SWIPE or abs(dif_y) > G2048.MINIMUM_SWIPE:
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
        scores = G2048.SCORES
        ind = scores.index(self.win_score)
        new_ind = (ind + 1) % len(scores)
        self.win_score = scores[new_ind]
        
    def start_game(self, *args):
        '''
        Start the game: resets the scores, rebuild the board, and add
        two new tiles.
        '''
        self.clear_widgets()
        self.active_game = True
        self.score = 0
        tamano = (self.ventana - G2048.SPACING) / 4
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
        new_tile.value = choice(G2048.NEW_TILE_SEQUENCE)
        
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
            self.save_last_position()
            if direction == 'right':
                for n, row in enumerate([2, 1, 0]):
                    Clock.schedule_once(partial(self.move_row_line, 
                                                direction, 
                                                self.get_full_tiles(row=row)),
                                        G2048.MOVE_DURATION*n)
            elif direction == 'left':
                for n, row in enumerate([1, 2, 3]):
                    Clock.schedule_once(partial(self.move_row_line, 
                                                direction, 
                                                self.get_full_tiles(row=row)),
                                        G2048.MOVE_DURATION*n)
            elif direction == 'up':
                for n, col in enumerate([2, 1, 0]):
                    Clock.schedule_once(partial(self.move_row_line, 
                                                direction, 
                                                self.get_full_tiles(col=col)),
                                        G2048.MOVE_DURATION*n)
            else:
                for n, col in enumerate([1, 2, 3]):
                    Clock.schedule_once(partial(self.move_row_line, 
                                                direction, 
                                                self.get_full_tiles(col=col)),
                                        G2048.MOVE_DURATION*n)
            Clock.schedule_once(self.end_of_move, G2048.MOVE_DURATION*3)
    
    def end_of_move(self, *args):
        '''
        Actions taken at the end of the move, once all tiles from all ros/cols
        have moved. In case no tile has moved these actions don't occur, 
        only the self._moving is reset to False. It is not considered a true
        move.

        This method is triggered after all the rows/tiles have moved, giving
        enough time for all the tiles to move before these actions take place.
        '''
        if self._moved_tile:
            self.add_tile()
            for child in self.children:
                child.merged = False
            self.end_of_game()
        self._moving = False
    
    def end_of_game(self):
        '''
        Check if game has finished, by one of the two situations: (1) one 
        tile reached the value of self.win_score, then player wins; (2) no
        moves are available, and no empty tiles, then player loses.

        If one of two situation arises, show popup and play the sound of
        winning or losing.

        Returns
        -------
        boolean
            True if the game has finished; False otherwise.
        '''
        if [child for child in self.children if child.value >= self.win_score]:
            # win game
            msg = 'Has ganado!'
            self.play('end_win')
        
        elif not self.available_moves():
            # no empty tiles --> lose game
            msg = 'Has perdido\nYa no puedes mover!'
            self.play('end_lose')
        
        else:
            return False
        
        PopupButton2048(title='Final', msg=msg)
        self.active_game = False
        return True
    
    def available_moves(self):
        '''
        Check if any moves are available. If some spaces are empty, it is
        considered that moves are available.
        
        Returns
        -------
        boolean
            True if there some moves are available, False otherwise
        '''
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
        '''
        Move all tiles in the row or line towards the direction.

        Arguments
        ---------
        direction : string
            Direction of the move. Can be 'up', 'down', 'left' or 'right'.
        row_line : list
            List of tiles that need to be moved.
        '''
        for tile in row_line:
            self.move_tile(direction, tile)
    
    def move_tile(self, direction, tile):
        '''
        Move the tile in the direction indicated. Check what is the final
        position, based on the other tiles in the board. If the position is
        different from current position, then:
            - change the tile to the new position,
            - add a new empty tile on the old position
            - merge the tile with the tile that was in the new position

        Arguments
        ---------
        direction : string
            Direction of the move. Can be 'up', 'down', 'left' or 'right'.
        tile : Tile
            Tiles to be moved.
        '''
        old_position = tile.position
        final_position = self.check_final(direction, old_position, tile.value)
        if final_position != old_position:
            self.add_widget(Tile(position=old_position, tamano=tile.tamano))        
            self.remove_widget(tile)
            self.add_widget(tile)  # to ensure it in on top
            tile_to_remove = self.get_tile(final_position)
            tile.position = final_position
            Clock.schedule_once(partial(self.end_of_move_tile, tile_to_remove, tile), 
                                G2048.MOVE_TILE)
    
    def end_of_move_tile(self, tile_to_remove, tile, *args):
        '''
        Execute actions after the tile has physically moved to the new 
        position: merge the value of the tile with that of previous tile,
        and remove the previous tile. And resets attribute _moved_tile to True

        Arguments
        ---------
        tile_to_remove : Tile
            Tile that has to be removed
        tile : Tile
            Tile that is moving
        '''
        tile.value += tile_to_remove.value
        self.remove_widget(tile_to_remove)
        self._moved_tile = True
        
    def check_final(self, direction, position, value):
        '''
        Return the final position to which the tile has to move. Recursive
        method, will check the tile next to it and trigger itself again until
        it reaches a stop value.

        Arguments
        ---------
        direction : string
            Direction of the move. Can be 'up', 'down', 'left' or 'right'.
        position: list or tuple (i, j)
            Position of the tile in the board grid.
        value : int
            value of the tile that is moving
        
        Returns
        -------
        position : list (i, j)
            Final position where the tile should be moved.

        '''
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
        '''
        Return the tile that is in the given position in the grid.

        Parameters
        ----------
        position : list
            Coordinates of position of tile in the grid
        
        Returns
        -------
        tile : Tile
            Tile that corresponds to the given position
        '''
        for child in self.children:
            if child.position == position:
                return child

    def save_last_position(self):
        '''
        Save the position of the board in a dictionary. This is called before 
        starting the move. The saved position can be used to go back to the 
        previous move.
        '''
        self.last_move = []
        for child in self.children:
            tile = dict()
            tile['value'] = child.value
            tile['position'] = child.position
            tile['tamano'] = child.tamano
            tile['score'] = self.score
            self.last_move.append(tile)            
            

    def back_button(self, *args):
        '''
        Move position of board to the position before the last move. Use the
        self.last_move
        '''
        if self.active_game:
            self.clear_widgets()
            for tile in self.last_move:
                obj = Tile(position=tile['position'], tamano=tile['tamano'])
                self.add_widget(obj)
                obj.value = tile['value']
                self.score -= tile['value']
            self.score = tile['score']

            
    def mute_button(self, *args):
        '''
        Toogle the mute button on / off.
        '''
        self.mute = not self.mute
            


