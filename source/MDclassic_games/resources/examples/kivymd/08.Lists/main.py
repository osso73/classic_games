#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivy.uix.scrollview import ScrollView



class DemoApp(MDApp):
    
    def build(self):
        screen = Screen()
        
        scroll = ScrollView()
        list_view = MDList()
        scroll.add_widget(list_view)
        
        # one line list items
        for n in range(5):
            items= OneLineListItem(text='Item ' + str(n))
            list_view.add_widget(items)
        
        # two line list items
        for n in range(5):
            items= TwoLineListItem(text='Item ' + str(n),
                                   secondary_text='Hello world')
            list_view.add_widget(items)
        
        # three line list items
        for n in range(5):
            items= ThreeLineListItem(text='Item ' + str(n),
                                   secondary_text='Hello world',
                                   tertiary_text='Yet another line')
            list_view.add_widget(items)
        
        screen.add_widget(scroll)

        return screen
   
    
if __name__ == '__main__':
    DemoApp().run()