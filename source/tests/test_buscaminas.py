#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 16:45:54 2020

@author: osso73
"""

import os
import pytest
import time

from buscaminas import main


class TestField():
    @pytest.fixture
    def field_with_mines_and_parent(self):
        class Parent(main.BoxLayout):
            class ids():
                class start_button():
                    def change_face(self, *args):
                        pass
        obj = main.Field()
        obj.mines = 10
        obj.columnas = 9
        obj.distribute_mines()
        parent = Parent()
        parent.add_widget(obj)
        return obj

    def test_start_game(self):
        obj = main.Field()
        obj.start_game()
        assert obj.mines == 10
        assert len(obj.children) == obj.columnas ** 2
        assert obj.game_active == True
        
    def test_tick(self):
        obj = main.Field()
        obj.game_active = True
        obj._start_time = time.time()
        time.sleep(1)
        obj.tick()
        assert obj.time == 1
        
    def test_distribute_mines(self, field_with_mines_and_parent):
        obj = field_with_mines_and_parent
        count = 0
        for child in obj.children:
            if child.value == 9:
                count += 1
        assert count == 10
        assert len(obj.children) == 81

 
    def test_find_adjacent_mines(self, field_with_mines_and_parent):
        data = [[0, 0, 0, 1, 9, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 9, 1],
                [2, 9, 1, 0, 0, 0, 2, 2, 2],
                [9, 3, 2, 1, 0, 0, 1, 9, 1],
                [2, 3, 9, 1, 0, 0, 1, 1, 1],
                [9, 3, 1, 1, 0, 1, 1, 1, 0],
                [9, 2, 0, 0, 0, 1, 9, 1, 0],
                [1, 1, 0, 1, 1, 2, 1, 1, 0],
                [0, 0, 0, 1, 9, 1, 0, 0, 0]]
        obj = field_with_mines_and_parent
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
    def test_find_neighbours(self, p_ref, n_ref, field_with_mines_and_parent):
        obj = field_with_mines_and_parent
        neighbour_list = obj.find_neighbours(p_ref)
        neighbour_list_pos =  {tuple(n.posicion) for n in neighbour_list}
        assert neighbour_list_pos == n_ref
        
    @pytest.mark.skip
    def test_check_uncover(self):
        '''cannot be checked'''
        pass
    
    def test_all_discovered(self, field_with_mines_and_parent):
        obj = field_with_mines_and_parent
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
    
    @pytest.fixture
    def field_with_parent(self, field_with_mines_and_parent):
        class Parent(main.BoxLayout):
            class ids():
                class start_button():
                    def change_face(self, *args):
                        pass

        obj = field_with_mines_and_parent
        parent = Parent()
        parent.add_widget(obj)
        return obj

    def test_game_lost(self, field_with_mines_and_parent):
        obj = field_with_mines_and_parent
        obj.game_active = True
        obj.game_lost()
        assert obj.game_active == False
        
    def test_game_won(self, field_with_mines_and_parent):
        obj = field_with_mines_and_parent
        obj.game_active = True
        obj.game_won()
        assert obj.game_active == False
        
    @pytest.mark.parametrize("blank_zone",[
        [(0,0), (1,0), (2,0)],
        [(3,2), (4,2), (5,2), (4,3), (5,3), (4,4), (5,4), (4,5), (2,6), (3,6), (4,6), (2,7), (0,8), (1,8), (2,8)],
        [(8,5), (8,6), (8,7), (8,8), (7,8), (6,8)],
        ])
    def test_no_adjacent_mines(self, field_with_mines_and_parent, blank_zone):
        data = [[0, 0, 0, 1, 9, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 9, 1],
                [2, 9, 1, 0, 0, 0, 2, 2, 2],
                [9, 3, 2, 1, 0, 0, 1, 9, 1],
                [2, 3, 9, 1, 0, 0, 1, 1, 1],
                [9, 3, 1, 1, 0, 1, 1, 1, 0],
                [9, 2, 0, 0, 0, 1, 9, 1, 0],
                [1, 1, 0, 1, 1, 2, 1, 1, 0],
                [0, 0, 0, 1, 9, 1, 0, 0, 0]]
        obj = field_with_mines_and_parent
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
    

    def test_open_adjacent(self, field_with_mines_and_parent):
        obj = field_with_mines_and_parent
        def get_tile_at_position(i, j, tiles):
            for t in tiles:
                if t.posicion == [i, j]:
                    return t
        data = [[0, 0, 0, 1, 9, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 9, 1],
                [2, 9, 1, 0, 0, 0, 2, 2, 2],
                [9, 3, 2, 1, 0, 0, 1, 9, 1],
                [2, 3, 9, 1, 0, 0, 1, 1, 1],
                [9, 3, 1, 1, 0, 1, 1, 1, 0],
                [9, 2, 0, 0, 0, 1, 9, 1, 0],
                [1, 1, 0, 1, 1, 2, 1, 1, 0],
                [0, 0, 0, 1, 9, 1, 0, 0, 0]]
        for t in obj.children:
            i, j = t.posicion
            t.value = data[j][i]
            t.uncovered = False
        
        tile = get_tile_at_position(5, 7, obj.children)
        for pos in [(6,6), (4,8)]:
            t = get_tile_at_position(*pos, obj.children)
            t.flag = True
        
        obj.open_adjacent(tile)
        for pos in [(4,7), (4,6), (5,6), (5,8), (6,8), (6,7)]:
            t = get_tile_at_position(*pos, obj.children)
            assert t.uncovered == True

        
        

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

    def test_set_show_with_name(self, area_with_parent):
        obj = area_with_parent
        obj.set_show(name='whatever-name')
        assert os.path.basename(obj.show) == 'whatever-name.jpg'
    
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
    
    @pytest.mark.skip
    def test_on_touch_down(self):
        '''cannot be tested'''


class TestStartButton():
    @pytest.mark.parametrize("touch", [
        ((200,200)), ((300,200)), ((200,300)), ((300,300)),
        ])
    def test_on_touch_down_true(self, touch):
        obj = main.StartButton()
        obj.size = (500, 500)
        obj.pos = (100, 100)
        assert 'standard' in obj.button_face
        class TouchPoint():
            pos = touch
        obj.on_touch_down(TouchPoint)
        assert 'standard' not in obj.button_face
        assert 'press' in obj.button_face

    @pytest.mark.parametrize("touch", [
        ((800,200)), ((300,900)), ((900,1200)), ((50,300)),
        ])
    def test_on_touch_down_false(self, touch):
        obj = main.StartButton()
        obj.size = (500, 500)
        obj.pos = (100, 100)
        class TouchPoint():
            pos = touch
        obj.on_touch_down(TouchPoint)
        assert 'standard' in obj.button_face
        assert 'press' not in obj.button_face


    @pytest.mark.skip
    def test_on_touch_up(self):
        '''cannot be checked'''
        pass

    def test_change_face_ok(self):
        obj = main.StartButton()
        options = ['lost', 'press', 'standard', 'won']
        for opt in options:
            obj.change_face(opt)
            assert opt in obj.button_face

    def test_change_face_error(self):
        obj = main.StartButton()
        options = ['new', 'non-existing']
        for opt in options:
            with pytest.raises(ValueError):
                obj.change_face(opt)

class TestMenuButton():
    @pytest.fixture
    def menu_button_with_size(self):
        obj = main.MenuButton()
        obj.size = (500, 500)
        obj.pos = (100, 100)
        obj.options = [f'option_{n+1}' for n in range(5)]
        obj.option = obj.options[0]
        return obj
        
    @pytest.mark.parametrize("touch", [
        ((200,200)), ((300,200)), ((200,300)), ((300,300)),
        ])
    def test_on_touch_down_true(self, menu_button_with_size, touch):
        obj = menu_button_with_size
        class TouchPoint():
            pos = touch
        result = obj.on_touch_down(TouchPoint)
        assert result == True
        assert 'hover' in obj.button_face
        for op in obj.options:
            assert op not in obj.button_face

    @pytest.mark.parametrize("touch", [
        ((800,200)), ((300,900)), ((900,1200)), ((50,300)),
        ])
    def test_on_touch_down_false(self, menu_button_with_size, touch):
        obj = menu_button_with_size
        class TouchPoint():
            pos = touch
        result = obj.on_touch_down(TouchPoint)
        assert result == None
        assert 'hover' not in obj.button_face


    @pytest.mark.parametrize("touch", [
        ((200,200)), ((300,200)), ((200,300)), ((300,300)),
        ])
    def test_on_touch_up_true(self, menu_button_with_size, touch):
        obj = menu_button_with_size
        class TouchPoint():
            pos = touch
        result = obj.on_touch_up(TouchPoint)
        assert result == True

    @pytest.mark.parametrize("touch", [
        ((800,200)), ((300,900)), ((900,1200)), ((50,300)),
        ])
    def test_on_touch_up_false(self, menu_button_with_size, touch):
        obj = menu_button_with_size
        class TouchPoint():
            pos = touch
        result = obj.on_touch_up(TouchPoint)
        assert result == None

    
    def test_change_option(self, menu_button_with_size):
        obj = menu_button_with_size
        for _ in range(2):
            for opt in obj.options:
                assert obj.option == opt
                obj.change_option()
            
