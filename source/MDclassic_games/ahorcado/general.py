#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 14:28:00 2021

@author: osso73
"""


def replace_letter(string, pos, letter):
    '''
    Replace the character in string in position pos, by letter.

    Attributes
    ----------
    string : string
        String of characters containing the text to be replaced
    pos : int
        Position to be replaced
    letter : string (1 character)
        Character that replaces the previous
    
    Returns
    -------
    string:
        the new string with the character replaced
    '''
    if pos > len(string):
        raise IndexError(f"pos > len(string) --> {pos} > {len(string)}")

    if len(letter) != 1:
        raise Exception("letter has to be a single character")
    
    return string[:pos] + letter + string[pos+1:]
