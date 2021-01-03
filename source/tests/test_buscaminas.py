#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:45:54 2020

@author: osso73
"""

import os
import pytest

from buscaminas import main


class TestField():
    def test_start_game(self):
        obj = main.Field()
        obj.start_game()
        assert obj.mines == 10
        assert len(obj.children) == obj.columnas ** 2
        
    @pytest.fixture
    def field_with_mines(self):
        obj = main.Field()
        obj.mines = 10
        obj.columnas = 9
        obj.distribute_mines()
        return obj
        
    def test_distribute_mines(self, field_with_mines):
        obj = field_with_mines
        count = 0
        for child in obj.children:
            if child.value == 9:
                count += 1
        assert count == 10
        assert len(obj.children) == 81

 
    def test_find_adjacent_mines(self, field_with_mines):
        data = [[0, 0, 0, 1, 9, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 9, 1],
                [2, 9, 1, 0, 0, 0, 2, 2, 2],
                [9, 3, 2, 1, 0, 0, 1, 9, 1],
                [2, 3, 9, 1, 0, 0, 1, 1, 1],
                [9, 3, 1, 1, 0, 1, 1, 1, 0],
                [9, 2, 0, 0, 0, 1, 9, 1, 0],
                [1, 1, 0, 1, 1, 2, 1, 1, 0],
                [0, 0, 0, 1, 9, 1, 0, 0, 0]]
        obj = field_with_mines
        for tile in obj.children:
            i, j = tile.posicion
            if data[j][i] == 9:
                tile.value = 9
            else:
                tile.value = 0
        
        obj.find_adjacent_mines()
        for tile in obj.children:
            i, j = tile.posicion
            assert tile.value == data[j][i]            


    @pytest.mark.parametrize('p_ref, n_ref', [
        ((0,0), {(0,1), (1,0), (1,1)}),
        ((0,8), {(0,7), (1,7), (1,8)}),
        ((8,0), {(7,0), (7,1), (8,1)}),
        ((8,8), {(7,8), (7,7), (8,7)}),
        ((0,4), {(0,3), (1,3), (1,4), (1,5), (0,5)}),
        ((4,0), {(3,0), (3,1), (4,1), (5,1), (5,0)}),
        ((8,3), {(8,2), (7,2), (7,3), (7,4), (8,4)}),
        ((3,8), {(2,8), (2,7), (3,7), (4,7), (4,8)}),
        ((2,2), {(1,1), (2,1), (3,1), (3,2), (3,3), (2,3), (1,3), (1,2)}),
        ((6,6), {(5,5), (6,5), (7,5), (7,6), (7,7), (6,7), (5,7), (5,6)}),
        ])
    def test_find_neighbours(self, p_ref, n_ref, field_with_mines):
        obj = field_with_mines
        neighbour_list = obj.find_neighbours(p_ref)
        neighbour_list_pos =  {tuple(n.posicion) for n in neighbour_list}
        assert neighbour_list_pos == n_ref
        
    @pytest.mark.skip
    def test_check_uncover(self):
        '''cannot be checked'''
        pass
    
    def test_all_discovered(self, field_with_mines):
        obj = field_with_mines
        assert obj.all_discovered() == False
        
        for area in obj.children:
            if area.value == 9:
                area.flag = True
            else:
                area.uncovered = True
        assert obj.all_discovered() == True
        
        if area.value == 9:
            area.flag = False
        else:
            area.uncovered = False
        assert obj.all_discovered() == False
    
    @pytest.mark.skip
    def test_game_lost(self):
        '''cannot be checked'''
        pass
    
    @pytest.mark.skip
    def test_game_won(self):
        '''cannot be checked'''
        pass
        
    @pytest.mark.parametrize("blank_zone",[
        [(0,0), (1,0), (2,0)],
        [(3,2), (4,2), (5,2), (4,3), (5,3), (4,4), (5,4), (4,5), (2,6), (3,6), (4,6), (2,7), (0,8), (1,8), (2,8)],
        [(8,5), (8,6), (8,7), (8,8), (7,8), (6,8)],
        ])
    def test_no_adjacent_mines(self, field_with_mines, blank_zone):
        data = [[0, 0, 0, 1, 9, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 9, 1],
                [2, 9, 1, 0, 0, 0, 2, 2, 2],
                [9, 3, 2, 1, 0, 0, 1, 9, 1],
                [2, 3, 9, 1, 0, 0, 1, 1, 1],
                [9, 3, 1, 1, 0, 1, 1, 1, 0],
                [9, 2, 0, 0, 0, 1, 9, 1, 0],
                [1, 1, 0, 1, 1, 2, 1, 1, 0],
                [0, 0, 0, 1, 9, 1, 0, 0, 0]]
        obj = field_with_mines
        for t in obj.children:
            i, j = t.posicion
            t.value = data[j][i]
            t.uncovered = False
            
        def get_tile_at_position(i, j, tiles):
            for t in tiles:
                if t.posicion == [i, j]:
                    return t
        
        for t_pos in blank_zone:
            t = get_tile_at_position(*t_pos, obj.children)
            obj.no_adjacent_mines(t)
            for pos in blank_zone:
                area = get_tile_at_position(*pos, obj.children)
                assert area.uncovered == True
    

class TestArea():
    @pytest.fixture
    def area_with_parent(self):
        class Parent(main.BoxLayout):
            mines = 10
            def check_uncover(self, *args):
                pass
            
            def all_discovered(self):
                return False
            
        parent = Parent()
        obj = main.Area()
        parent.add_widget(obj)
        return obj

    @pytest.mark.parametrize("flag, uncovered, value, show",[
        (True, True, 3, '3.jpg'),
        (True, False, 2, 'bandera.jpg'),
        (False, True, 5, '5.jpg'),
        (False, False, 1, 'covered.jpg'),
        ])
    def test_set_show(self, area_with_parent, flag, uncovered, value, show):
        obj = area_with_parent
        obj.value = value
        obj.uncovered = uncovered
        obj.flag = flag
        obj.set_show()
        assert os.path.basename(obj.show) == show
    
    def test_on_flag(self, area_with_parent):
        obj = area_with_parent
        obj.flag = False
        obj.uncovered = False
        for _ in range(2):
            assert os.path.basename(obj.show) == 'covered.jpg'
            assert obj.parent.mines == 10
            obj.switch_flag()
            assert os.path.basename(obj.show) == 'bandera.jpg'
            assert obj.parent.mines == 9
            obj.switch_flag()
        
    def test_switch_flag(self, area_with_parent):
        obj = area_with_parent
        for n in range(2):
            obj.switch_flag()
            assert obj.flag == True
            assert obj.parent.mines == 9
            obj.switch_flag()
            assert obj.flag == False
            assert obj.parent.mines == 10
    
    def test_on_uncovered(self, area_with_parent):
        obj = area_with_parent
        obj.uncovered = False
        obj.value = 5
        assert os.path.basename(obj.show) == 'covered.jpg'
        obj.uncover()
        assert os.path.basename(obj.show) == '5.jpg'
    
    def test_uncover(self, area_with_parent):
        obj = area_with_parent
        obj.uncovered = False
        obj.uncover()
        assert obj.uncovered == True
        obj.uncover()
        assert obj.uncovered == True
            