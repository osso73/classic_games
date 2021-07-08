#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 12:22:14 2021

@author: osso73
"""

# std libraries


# non-std libraries


# my app imports
import snake.constants as SNAKE



class Level():
    '''
    Control the levels: building the walls, location and direction of the 
    snake at the start, maximum punctuation of each level, and progress.
    
    Attributes
    ----------
    max_level : int
        Number of the highest level available. Used to control when game is 
        finished (i.e. no more levels available)
    num_level : int
        Current level number.
    grid : list (n, m)
        Size of the grid used (in squares, not in pixels). Used to calculate
        positions of the walls and snake.
    level_max_score : int
        Maximum score for the current level, based on the size of the grid.
    level_curr_score : int
        Score for the level. Initialised to 0 at the start of the level.
    level_pct : float
        Percentage of the level progress.
    
    '''

    def __init__(self, grid, num=1, *args):
        super(Level, self).__init__(*args)
        self.max_level = 12
        self.grid = grid
        self.num_level = num
        self.level_curr_score = 0
        self.level_pct = 0
        self.level_max_score = self.get_max_score()

    
    def get_max_score(self):
        '''
        Return maximum score of the level, based on the grid size and 
        the level number.

        Returns
        -------
        int
            Maximum score of the level.

        '''
        MAX = {11: 25, 15:32, 19:40, 23:50}
        num = min(*self.grid) + 1
        return MAX[num]

    
    def get_walls(self):
        '''
        Select the build function corresponding to the current level, and 
        return the result.

        Returns
        -------
        list
            List of positions whew there is a wall.

        '''
        build_func = [self.build_walls01, self.build_walls02, 
                      self.build_walls03, self.build_walls04,
                      self.build_walls05, self.build_walls06,
                      self.build_walls07, self.build_walls08,
                      self.build_walls09, self.build_walls10,
                      self.build_walls11, self.build_walls12]
        return build_func[self.num_level-1]()


    def get_start_position(self):
        '''
        Return the start position of the snake, based on the current level.

        Returns
        -------
        tupple
            Tupple of ints, corresponding to the grid position of start.

        '''
        n, m = self.grid
        n_factor, m_factor = SNAKE.LEVEL_PARAMETERS[self.num_level]['pos_ini']
        if n > m:  # swap factors in case of landscape layout
            n_factor, m_factor = 1-m_factor, 1-n_factor
        return int(n * n_factor), int(m * m_factor)
        
            
    def get_start_direction(self):
        '''
        Return the start direction of the snake, based on the current level.

        Returns
        -------
        d : string
            Direction. Can be one of ['UP', 'DOWN', 'LEFT', 'RIGHT'].

        '''
        d = SNAKE.LEVEL_PARAMETERS[self.num_level]['dir']
        n, m = self.grid
        if n > m:  # swap direction in case of landscape layout
            d = 'RIGHT' if d == 'DOWN' else 'DOWN'
        return d

    
    def set_level(self, num):
        '''
        Set the level in self.num_level, and load the variable max_score, and
        reset the current score.        

        Parameters
        ----------
        num : int
            Level number.

        '''
        self.num_level = num
        self.level_max_score = self.get_max_score()
        self.level_curr_score = 0
        self.level_pct = self.level_curr_score / self.level_max_score

        
    def inc_score(self, num):
        '''Increase the score by num, and recalculate percentage'''
        
        self.level_curr_score += num
        self.level_pct = self.level_curr_score / self.level_max_score

            
    def build_walls01(self):
        '''Build function for level 1. Return list of positions of wall.'''
        
        return []


    def build_walls02(self):
        '''Build function for level 2. Return list of positions of wall.'''

        return self.build_one_short_line(0.5)


    def build_walls03(self):
        '''Build function for level 3. Return list of positions of wall.'''

        return self.build_one_long_line(0.5)


    def build_walls04(self):
        '''Build function for level 4. Return list of positions of wall.'''

        positions = self.build_one_short_line(1/3)
        positions += self.build_one_short_line(-1/3)
        return positions


    def build_walls05(self):
        '''Build function for level 5. Return list of positions of wall.'''

        positions = self.build_one_long_line(1/3)
        positions += self.build_one_long_line(-1/3)
        return positions


    def build_walls06(self):
        '''Build function for level 6. Return list of positions of wall.'''

        positions = self.build_one_long_line(0.5)
        positions += self.build_one_short_line(1/3)
        positions += self.build_one_short_line(-1/3)
        return positions


    def build_walls07(self):
        '''Build function for level 7. Return list of positions of wall.'''

        positions = self.build_one_long_line(1/3)
        positions += self.build_one_long_line(-1/3)
        positions += self.build_one_short_line(0.5)
        return positions


    def build_walls08(self):
        '''Build function for level 8. Return list of positions of wall.'''

        return self.build_around()


    def build_walls09(self):
        '''Build function for level 9. Return list of positions of wall.'''

        positions = self.build_around()
        positions += self.build_one_long_line(0.5)
        return positions


    def build_walls10(self):
        '''Build function for level 10. Return list of positions of wall.'''

        positions = self.build_around()
        positions += self.build_one_short_line(1/3)
        positions += self.build_one_short_line(-1/3)
        return positions


    def build_walls11(self):
        '''Build function for level 11. Return list of positions of wall.'''

        positions = self.build_around()
        positions += self.build_one_short_line(1/3)
        positions += self.build_one_short_line(-1/3)
        positions += self.build_one_long_line(0.5)
        return positions


    def build_walls12(self):
        '''Build function for level 12. Return list of positions of wall.'''

        positions = self.build_around()
        positions += self.build_one_short_line(1/4)
        positions += self.build_one_short_line(2/4)
        positions += self.build_one_short_line(-1/4)
        return positions


    def build_around(self):
        '''
        Build function to build walls around the screen, with holes. Used by
        the functions to build the levels.
        
        Returns
        -------
        positions : list
            List of grid coordinates where there is a wall.
                
        '''
        n_max, m_max = self.grid
        n_list = [n for n in range(n_max+1)]
        m_list = [m for m in range(m_max+1)]
        
        positions = []
        if n_max < m_max:
            idx = int((n_max + 1) / 3)
            n_list = n_list[:idx] + n_list[-idx:]
            idx = int((m_max + 1) / 6)
            m_list = m_list[:idx] + m_list[2*idx:-2*idx] + m_list[-idx:]
        else:
            idx = int((m_max + 1) / 3)
            m_list = m_list[:idx] + m_list[-idx:]
            idx = int((n_max + 1) / 6)
            n_list = n_list[:idx] + n_list[2*idx:-2*idx] + n_list[-idx:]
            
        for i in n_list:
            positions.append([i, 0])
            positions.append([i, m_max])
        
        for j in m_list:
            positions.append([0, j])
            positions.append([n_max, j])

        return positions


    def build_one_short_line(self, pct):
        '''
        Build function to build a short line of wall, located at pct of the 
        screen. Used by the functions to build the levels.
        
        Parameters
        ----------
        pct : float
            Percentage of the screen where the line is located. E.g. 0.5 means
            the line is in the middle of the grid.
        
        Returns
        -------
        positions : list
            List of grid coordinates where there is a wall.
        
        '''
        n_max, m_max = self.grid
        n_list = [n for n in range(n_max+1)]
        m_list = [m for m in range(m_max+1)]
        n_pct = int(n_max * pct)
        m_pct = int(m_max * pct)
        if n_pct < 0:
            n_pct -= 1
        if m_pct < 0:
            m_pct -= 1

        positions = []
        if n_max < m_max:
            idx = int((n_max + 1) / 3)
            n_list = n_list[idx:-idx]
            m = m_list[m_pct]
            for n in n_list:
                positions.append([n, m])
        else:
            idx = int((m_max + 1) / 3)
            m_list = m_list[idx:-idx]
            n = n_list[n_pct]
            for m in m_list:
                positions.append([n, m])
        
        return positions
        

    def build_one_long_line(self, pct):
        '''
        Build function to build a long line of wall, located at pct of the 
        screen. Used by the functions to build the levels.
        
        Parameters
        ----------
        pct : float
            Percentage of the screen where the line is located. E.g. 0.5 means
            the line is in the middle of the grid.
        
        Returns
        -------
        positions : list
            List of grid coordinates where there is a wall.
        
        '''
        n_max, m_max = self.grid
        n_list = [n for n in range(n_max+1)]
        m_list = [m for m in range(m_max+1)]
        n_pct = int(n_max * pct)
        m_pct = int(m_max * pct)
        if n_pct < 0:
            n_pct -= 1
        if m_pct < 0:
            m_pct -= 1

        positions = []
        if n_max > m_max:
            idx = int((n_max + 1) / 3)
            n_list = n_list[idx:-idx]
            m = m_list[m_pct]
            for n in n_list:
                positions.append([n, m])
        else:
            idx = int((m_max + 1) / 3)
            m_list = m_list[idx:-idx]
            n = n_list[n_pct]
            for m in m_list:
                positions.append([n, m])
        
        return positions


if __name__ == '__main__':
    print('Class definition only -- not to be executed.')