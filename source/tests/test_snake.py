#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:45:54 2020

@author: osso73
"""

import os
import sys
import time
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'snake')))

from snake import main


class TestMainScreen():
    pass


class TestGameBoard():
        
    @pytest.mark.skip(reason="function cannot be tested")
    def test_on_speed(self):
        pass
    
    @pytest.mark.parametrize('screen_fixture', [
        (320, 240), (820, 540), (3000, 3000), (240, 320), (540, 820)
        ])
    @pytest.mark.parametrize('snake_fixture', [*main.GRID_SIZES])
    def test_set_size(self, screen_fixture, snake_fixture):
        parent = main.Widget()
        game = main.GameBoard()
        parent.add_widget(game)
        parent.size = screen_fixture
        game.size_snake = snake_fixture
        game.set_size()
        
        # calculate values
        pix = int(0.95 * min(*screen_fixture) / snake_fixture)
        n = int(0.95 * screen_fixture[0] / pix)
        m = int(0.95 * screen_fixture[1] / pix)
        
        # ensure minimum value corresponds with snake_fixture
        if n < m:
            n = snake_fixture
        else:
            m = snake_fixture
        
        assert game.size_pixels == pix
        assert game.size == [n*pix, m*pix]
        assert [n-1, m-1] == game.size_grid
    
    
    def test_start_game_reset(self):
        '''
        cannot be tested because Food is defined with grid variable in 
        kv file
        '''
        parent = main.Widget()
        game = main.GameBoard()
        parent.add_widget(game)
        parent.size = 1920, 1080
        
        game.snake_parts = [3,6,8,1,5,3,2]
        game.score = 28
        game.start_game()
        assert game.score == 0
        assert len(game.snake_parts) == 4
        for part in game.snake_parts:
            assert isinstance(part, [SnakeHead, SnakePart])
        
