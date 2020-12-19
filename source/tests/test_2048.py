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
        
        num = randint(1, 12)
        for _ in range(num):
            board_with_tiles.add_tile()
        empty_tiles = board_with_tiles.get_empty_tiles()
        assert len(empty_tiles) == 12 - num
        
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



