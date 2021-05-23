#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.list import MDList, ThreeLineListItem, ThreeLineIconListItem
from kivymd.uix.list import IconLeftWidget, ImageLeftWidget
from kivy.uix.scrollview import ScrollView



class DemoApp(MDApp):
    '''
    You need to import the LineIconListItem corresponding to the number
    of lines you are using (e.g. One, Two or Three).
    
    You can use avatars (e.g. images) instead of icon. Just need to use
    ImageLeftWidget. Note that ImageRightWidget and IconRightWidget are not 
    properly implemented in Kivymd
    '''
    def build(self):
        screen = Screen()
        
        scroll = ScrollView()
        list_view = MDList()
        scroll.add_widget(list_view)
        
        # icons
        for n in range(5):
            icon = IconLeftWidget(icon='language-python')
            items = ThreeLineIconListItem(text='Item ' + str(n),
                                   secondary_text='Hello world',
                                   tertiary_text='Yet another line')
            items.add_widget(icon)
            list_view.add_widget(items)
        
        # images
        for n in range(5):
            image = ImageLeftWidget(source=f'user-{n}.png')
            items = ThreeLineIconListItem(text='Item ' + str(n),
                                   secondary_text='Hello world',
                                   tertiary_text='Yet another line')
            items.add_widget(image)
            list_view.add_widget(items)

        screen.add_widget(scroll)

        return screen
   
    
if __name__ == '__main__':
    DemoApp().run()