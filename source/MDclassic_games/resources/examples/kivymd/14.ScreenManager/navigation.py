# -*- coding: utf-8 -*-

screen_helper = '''
ScreenManager:         
    MenuScreen:
    ProfileScreen:
    UploadScreen:

<MenuScreen>:
    name: 'menu'
    MDRectangleFlatButton:
        text: 'Profile'
        pos_hint: {'center_x': 0.5, 'center_y': 0.35}
        on_release: root.manager.current = 'profile'

    MDRectangleFlatButton:
        text: 'Upload'
        pos_hint: {'center_x': 0.5, 'center_y': 0.65}
        on_release: root.manager.current = 'upload'


<ProfileScreen>:
    name: 'profile'
    MDLabel:
        text: 'Welcome Susana'
        halign: 'center'

    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x': 0.5, 'center_y': 0.25}
        on_release: root.manager.current = 'menu'



<UploadScreen>:
    name: 'upload'
    MDLabel:
        text: "Let's upload some files"
        halign: 'center'

    MDRectangleFlatButton:
        text: 'Back'
        pos_hint: {'center_x': 0.5, 'center_y': 0.25}
        on_release: root.manager.current = 'menu'


'''
