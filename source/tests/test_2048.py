#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 20:44:48 2020

@author: osso73
"""

import pytest
from twenty_fortyeight import main
from collections import namedtuple
from random import randint

Point = namedtuple('Point', 'x y')

class TestTile():        
    def test_calc_position(self):
        obj = main.Tile()
        obj.position = [2, 3]
        obj.tamano = 10
        pos = obj.calc_position()
        assert pos == (20+main.SPACING, 30+main.SPACING)
    
    def test_on_position(self):
        assert True
    
    def text_on_value(self):
        assert True


class TestBoard():        
    def test_attributes(self):
        obj = main.Board()
        assert obj.ventana == 0
        assert obj.win_score == 2048
        assert obj.score == 0
        assert obj.active_game == False
        assert obj.last_move == []
        assert obj._moving == False
        assert obj._moved_tile == False

    @pytest.mark.skip  # test does not work (?)
    def test_initialize_grid(self):
        box = main.BoxLayout()
        box.size = (300, 400)
        box.add_widget(main.Board())
        board = box.children[0]
        assert board.ventana == 300

    @pytest.fixture
    def board_with_size(self):
        obj = main.Board()
        obj.size = 300, 300
        obj.pos = 100, 100
        return obj

    def test_touch_down(self, board_with_size):
        touch = Point(200,300)
        board_with_size.on_touch_down(touch)
        assert board_with_size.swipe_x == 200
        assert board_with_size.swipe_y == 300

    @pytest.mark.parametrize("touch_up, dir_move", [
        ((140, 300), 'left'), ((140, 320), 'left'), 
        ((260, 300), 'right'), ((260, 330), 'right'), 
        ((200, 360), 'up'), ((240, 360), 'up'), 
        ((200, 210), 'down'), ((240, 210), 'down'),
        ((200, 260), None), ((240, 320), None),
        ])
    def test_swipe_all(self, board_with_size, touch_up, dir_move):
        touch = Point(200,300)
        board_with_size.on_touch_down(touch)
        touch = Point(*touch_up)        
        direction = board_with_size.on_touch_up(touch)
        assert direction == dir_move

        touch = Point(200,300)
        board_with_size.on_touch_down(touch)
        touch = Point(*touch_up)        
        direction = board_with_size.on_touch_up(touch)
        assert direction == dir_move

    def test_change_win_score(self):
        obj = main.Board()
        
        # execute twice, to test rolling out ok
        for _ in [0, 1]:
            for n in range(len(main.SCORES)):
                obj.change_win_score()
                assert obj.win_score == main.SCORES[n]

    def test_start_game(self):
        obj = main.Board()
        obj.start_game()
        assert obj.score == 0
        assert len(obj.children) == 16
        
        non_empty = 0
        for tile in obj.children:
            if tile.value != 0:
                non_empty += 1
        assert non_empty == 2
    
    @pytest.fixture
    def board_with_tiles(self):
        '''
        return board with num tiles. num needs to be passed
        as a parameter.
        '''
        def _method(num):
            obj = main.Board()
            obj.start_game()
            if num > 2:
                for _ in range(num-2):
                    obj.add_tile()
            return obj
        
        return _method

    def test_add_tile(self, board_with_tiles):
        non_empty = 0
        for tile in board_with_tiles(4).children:
            if tile.value != 0:
                non_empty += 1
        assert non_empty == 4

    def test_empty_tiles(self, board_with_tiles):
        empty_tiles = board_with_tiles(4).get_empty_tiles()
        assert len(empty_tiles) == 12
        
        num = randint(2, 16)
        empty_tiles = board_with_tiles(num).get_empty_tiles()
        assert len(empty_tiles) == 16 - num
        
    def test_get_full_tiles_all(self, board_with_tiles):
        for n in range(2, 16):
            full = board_with_tiles(n).get_full_tiles()
            assert len(full) == n
    
    def test_get_full_tiles_row(self, board_with_tiles):
        board = board_with_tiles(16)
        row = randint(0, 3)
        tiles = board.get_full_tiles(row=row)
        assert len(tiles) == 4
        for tile in tiles:
            assert tile.position[0] == row

    def test_get_full_tiles_col(self, board_with_tiles):
        board = board_with_tiles(16)
        col = randint(0, 3)
        tiles = board.get_full_tiles(col=col)
        assert len(tiles) == 4
        for tile in tiles:
            assert tile.position[1] == col

    def test_move(self):
        '''can't test anything'''
        assert True
    
    def test_end_of_move(self, board_with_tiles):
        board = board_with_tiles(12)
        for child in board.children:
            child.merged = True
        board._moving = True
        
        # if no tile moved, tiles are not reset
        board._moved_tile == False
        board.end_of_move()
        assert board._moving == False
        for child in board.children:
            assert child.merged == True
        
        # if some tile moved, all tiles are reset
        board._moved_tile = True
        board.end_of_move()
        assert board._moving == False
        for child in board.children:
            assert child.merged == False

    @pytest.mark.skip  # cannot find running_app, so it gives error
    def test_end_of_game(self, board_with_tiles):
        board = board_with_tiles(2)
        assert board.end_of_game() == False
        
        board.children[3].value = board.win_score
        assert board.end_of_game() == True

        # fill all values, no move possible
        for child in board.children:
            i, j = child.position
            child.value = (i + j) % 2 + 2
        assert board.end_of_game() == True

        # fill all values, some moves possible
        for child in board.children:
            i, j = child.position
            if i == 2:
                child.value = 2
            else:
                child.value = (i + j) % 2 + 2
        assert board.end_of_game() == False

    def test_available_moves(self, board_with_tiles):
        board = board_with_tiles(2)
        assert board.available_moves() == True

        # fill all values, no move possible
        for child in board.children:
            i, j = child.position
            child.value = (i + j) % 2 + 2
        assert board.available_moves() == False

        # fill all values, some moves possible
        for child in board.children:
            i, j = child.position
            if i == 2:
                child.value = 2
            else:
                child.value = (i + j) % 2 + 2
        assert board.available_moves() == True

    def test_move_row_line(self):
        '''cannot be tested'''
        assert True
    
    def test_move_tile(self):
        '''cannot be tested'''
        assert True

    def test_end_of_move_tile(self, board_with_tiles):
        board = board_with_tiles(2)
        tile, tile_to_remove = board.get_full_tiles()
        tile.value = 8 
        tile_to_remove.value = 12
        assert board._moved_tile == False

        board.end_of_move_tile(tile_to_remove, tile)
        assert board._moved_tile == True
        assert tile.value == 20

    @pytest.mark.parametrize("pos_i, direction, pos_f", [
        ([0, 1], 'right', [3, 1]), ([1, 3], 'down', [1, 0]), 
        ([3, 2], 'left', [0, 2]), ([2,1], 'up', [2,3]) 
        ])  
    def test_check_final_notiles(self, board_with_tiles, pos_i, 
                                 direction, pos_f):
        board = board_with_tiles(2)
        for child in board.children:
            child.value = 0
        final = board.check_final(direction, pos_i, 2)
        assert final == pos_f

    def test_check_final_merge(self, board_with_tiles):
        board = board_with_tiles(2)
        for child in board.children:
            if child.position == [3, 1]:
                child.value = 2
            else:
                child.value = 0
        final = board.check_final('right', (1, 1), 2)
        assert final == [3, 1]
        final = board.check_final('right', (1, 1), 4)
        assert final == [2, 1]
        
    def test_get_tile(self, board_with_tiles):
        board = board_with_tiles(16)
        for i in range(4):
            for j in range(4):
                tile = board.get_tile([i, j])
                assert tile.position == [i, j]
    
    def test_save_last_position(self, board_with_tiles):
        board = board_with_tiles(16)
        board.last_move = []
        board.save_last_position()
        assert len(board.last_move) == 16
        for tile in board.last_move:
            t = board.get_tile(tile['position'])
            assert t.value == tile['value']

    def test_back_button(self, board_with_tiles):
        board = board_with_tiles(8)
        board.save_last_position()
        initial_position = board.last_move
        
        #change board
        for tile in board.children:
            tile.value += 5
        
        board.back_button()
        for tile in initial_position:
            t = board.get_tile(tile['position'])
            assert t.value == tile['value']
    
class TestMainScreen():
    def test_load_sounds(self):
        obj = main.MainScreen()
        sounds = obj.load_sounds()
        sound_list = ['move', 'end_win', 'end_lose']
        for s in sounds:
            assert s in sound_list
        
        for s in sound_list:
            assert s in sounds
        