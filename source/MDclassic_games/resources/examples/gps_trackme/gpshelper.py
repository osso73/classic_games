#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  2 17:57:34 2021

@author: oriol
"""


# std libraries
from kivy.app import App
from kivy.utils import platform
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton

# non-std libraries

# my app imports





class GpsHelper():
    
    def stop(self):
        if platform == 'android':
            from plyer import gps
            try:
                gps.stop()
            except Exception:
                pass


    def run(self):

        # Request permissions on Android
        if platform == 'android':
            from android.permissions import Permission, request_permissions
            def callback(permission, results):
                if all([res for res in results]):
                    print("Got all permissions")
                    from plyer import gps
                    gps.configure(on_location=self.update_gps_position,
                                  on_status=self.on_auth_status)
                    gps.start(minTime=1000, minDistance=0)
                else:
                    print("Did not get all permissions")

            request_permissions([Permission.ACCESS_COARSE_LOCATION,
                                 Permission.ACCESS_FINE_LOCATION], callback)
        


    def update_gps_position(self, *args, **kwargs):
        my_lat = float(kwargs['lat'])
        my_lon = float(kwargs['lon'])
        accuracy = float(kwargs['accuracy'])
        
        app = MDApp.get_running_app()
        topbar = app.root.ids.topbar
        label = app.root.ids.label
        mymap = app.root.ids.mapview
        gps_blinker = mymap.ids.blinker
        
        # Update label
        label.lat = my_lat
        label.lon = my_lon
        
        # Update map and blinker
        gps_blinker.lat = my_lat
        gps_blinker.lon = my_lon
        if mymap.center_map:
            mymap.center_on(my_lat, my_lon)
        
        # Update icons for gps and accuracy
        topbar.gps_status = 'on'
        topbar.accuracy = accuracy
        

    def on_auth_status(self, general_status, status_message):        
        if general_status != 'provider-enabled':
            app = MDApp.get_running_app()
            topbar = app.root.ids.topbar
            topbar.gps_status = 'off'
            self.open_gps_access_popup()


    def open_gps_access_popup(self):        
        txt = "You need to enable GPS access for the app to function properly"
        dialog = MDDialog(title="GPS Error", text=txt, size_hint = [.8, .8], 
                          pos_hint = {'center_x': .5, 'center_y': .5})
        dialog.open()
