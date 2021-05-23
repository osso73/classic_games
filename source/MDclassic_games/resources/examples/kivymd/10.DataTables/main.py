#!/usr/bin/env python
# -*- coding: utf-8 -*-

from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp


class DemoApp(MDApp):
    
    def build(self):
        screen = Screen()
        table = MDDataTable(size_hint=(0.9, 0.6), 
                            check=True,
                            rows_num=15,
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            column_data=[
                                ("Id", dp(18)),
                                ("Food", dp(20)),
                                ("Calories", dp(20))
                            ],
                            row_data=[
                                ('1', 'Burger', '300'),
                                ('2', 'Oats', 150) ,           
                                ('3', 'Oats', 150) ,           
                                ('4', 'Oats', 150) ,           
                                ('5', 'Oats', 150) ,           
                                ('6', 'Oats', 150) ,           
                                ('7', 'Oats', 150) ,           
                                ('8', 'Oats', 150) ,           
                                ('9', 'Oats', 150) ,           
                                ('10', 'Oats', 150) ,           
                                ('11', 'Oats', 150) ,           
                                ('12', 'Oats', 150) ,           
                            ]
                            )
        table.bind(on_row_press=self.on_row_press)
        table.bind(on_check_press=self.on_check_press)
        screen.add_widget(table)
        return screen
    
    def on_row_press(self, instance_table, instance_row):
        print("row_press: ", instance_table, instance_row)

    def on_check_press(self, instance_table, current_row):
        print("check_press: ", instance_table, current_row)



if __name__ == '__main__':
    DemoApp().run()
