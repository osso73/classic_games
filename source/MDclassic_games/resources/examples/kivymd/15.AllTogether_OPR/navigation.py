# -*- coding: utf-8 -*-

navigation_helper = '''
Screen:
    NavigationLayout:
        ScreenManager:
            id: screen_manager
            MenuScreen:
            ProfileScreen:
            UploadScreen:
                                                
        MDNavigationDrawer:
            id: nav_drawer
            BoxLayout:
                orientation: 'vertical'
                spacing: '8dp'
                padding: '8dp'
                Image:
                    source: 'picture.png'
                
                MDLabel:
                    text: '  Susana'
                    font_style: 'Subtitle1'
                    size_hint_y: None
                    height: self.texture_size[1]
                
                MDLabel:
                    text: '  pastor.librada@gmail.com'
                    font_style: 'Caption'
                    size_hint_y: None
                    height: self.texture_size[1]
                
                ScrollView:
                    MDList:
                        OneLineIconListItem:
                            text: 'Main'
                            on_release:
                                nav_drawer.set_state("close")
                                screen_manager.current = 'menu'
                            IconLeftWidget:
                                icon: 'coffee'
                            
                        OneLineIconListItem:
                            text: 'Profile'
                            on_release:
                                nav_drawer.set_state("close")
                                screen_manager.current = 'profile'
                            IconLeftWidget:
                                icon: 'face-profile'
                            
                        OneLineIconListItem:
                            text: 'Upload'
                            on_release:
                                nav_drawer.set_state("close")
                                screen_manager.current = 'upload'
                            IconLeftWidget:
                                icon: 'upload'
                        OneLineIconListItem:
                            text: 'Logout'
                            on_release: app.stop()
                            IconLeftWidget:
                                icon: 'logout'


<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: 'Demo'
            elevation: 8
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        BoxLayout:
            orientation: 'vertical'
            padding: '10dp'
            
            MDLabel:
                text: 'Welcome to this demo'
                halign: 'center'
                font_style: 'H3'

            MDLabel:
                text: 'Open the menu to proceed, or click the buttons below'
                halign: 'center'
            
            FloatLayout:
                orientation: 'horizontal'
                
                MDFlatButton:
                    text: 'Profile'
                    pos_hint: {'center_x': 0.25, 'center_y': 0.5} 
                    on_release: root.manager.current = 'profile'
                    
                MDFlatButton:
                    text: 'Upload'
                    pos_hint: {'center_x': 0.75, 'center_y': 0.5}
                    on_release: root.manager.current = 'upload'

<ProfileScreen>:
    name: 'profile'
    BoxLayout:
        orientation: 'vertical'

        MDToolbar:
            title: 'Demo'
            elevation: 10
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]

        FloatLayout:
            
            MDLabel:
                text: 'Profile screen'
                font_style: 'H3'
                pos_hint: {'center_x': 0.5, 'center_y': 0.75}
                halign: 'center'
        
            MDLabel:
                text: 'Welcome Susana'
                halign: 'center'
        
            MDRectangleFlatButton:
                text: 'Back'
                pos_hint: {'center_x': 0.5, 'center_y': 0.25}
                on_release: root.manager.current = 'menu'



<UploadScreen>:
    name: 'upload'
    
    BoxLayout:
        orientation: 'vertical'
        
        MDToolbar:
            title: 'Demo'
            elevation: 10
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("open")]]
    
        FloatLayout:
            
            MDLabel:
                text: 'Upload screen'
                font_style: 'H3'
                pos_hint: {'center_x': 0.5, 'center_y': 0.75}
                halign: 'center'
                
            MDLabel:
                text: "Let's upload some files"
                halign: 'center'
        
            MDRectangleFlatButton:
                text: 'Back'
                pos_hint: {'center_x': 0.5, 'center_y': 0.25}
                on_release: root.manager.current = 'menu'



'''