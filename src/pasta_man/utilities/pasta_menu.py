#
# This file contains class __menu for Pasta-Man
#

from os.path import join as jPath, exists as there
from pathlib import Path
from tkinter import *
import ttkthemes
import threading
import sys

import ttkthemes.themed_style

class __menu__:
    def __init__(self, menuparent: Menu):
        self.parent = menuparent
        
        # set style -> theme -> default: arc
        if not there(jPath(str(Path.home()), '.pastaman', '.defaulttheme')):
            self.style:ttkthemes.themed_style.ThemedStyle = ttkthemes.themed_style.ThemedStyle(theme='arc')
        else:
            with open(jPath(str(Path.home()), '.pastaman', '.defaulttheme'), 'r') as theme:
                self.defaultTheme = theme.read().replace('\n', '')
                self.style:ttkthemes.themed_style.ThemedStyle = ttkthemes.themed_style.ThemedStyle(theme=self.defaultTheme)
    
    def Themes(self):
        ThemeMenu = Menu(self.parent)
        
        self.parent.add_cascade(label="Themes", menu=ThemeMenu)
        
        # Themes Functions #
        def savetheme(theme:str):
            with open(jPath(str(Path.home()), '.pastaman', '.defaulttheme'), 'w') as themefile:
                themefile.write(theme)
            sys.exit(0)
            
        def changeThemeToKroc():
            self.style.theme_use('kroc')
            threading.Thread(target=savetheme, args=('kroc',)).start()
        
        def changeThemeToKeramik():
            self.style.theme_use('keramik')
            threading.Thread(target=savetheme, args=('keramik',)).start()
        
        def changeThemeToEquilux():
            self.style.theme_use('equilux')
            threading.Thread(target=savetheme, args=('equilix',)).start()
        
        def changeThemeToElegance():
            self.style.theme_use('elegance')
            threading.Thread(target=savetheme, args=('elegance',)).start()
        
        def changeThemeToClearlooks():
            self.style.theme_use('clearlooks')
            threading.Thread(target=savetheme, args=('clearlooks',)).start()
        
        def changeThemeToBreeze():
            self.style.theme_use('breeze')
            threading.Thread(target=savetheme, args=('breeze',)).start()
        
        def changeThemeToBlue():
            self.style.theme_use('blue')
            threading.Thread(target=savetheme, args=('blue',)).start()
        
        def changeThemeToBlack():
            self.style.theme_use('black')
            threading.Thread(target=savetheme, args=('black',)).start()
        
        def changeThemeToAquativo():
            self.style.theme_use('aquativo')
            threading.Thread(target=savetheme, args=('aquativo',)).start()
        
        def changeThemeToArc():
            self.style.theme_use('arc')
            threading.Thread(target=savetheme, args=('arc',)).start()
        
        def changeThemeToAdapta():
            self.style.theme_use('adapta')
            threading.Thread(target=savetheme, args=('adapta',)).start()
        
        def changeThemeToPlastik():
            self.style.theme_use('plastik')
            threading.Thread(target=savetheme, args=('plastik',)).start()
        
        def changeThemeToRadiance():
            self.style.theme_use('radiance')
            threading.Thread(target=savetheme, args=('radiance',)).start()
        
        def changeThemeToSmog():
            self.style.theme_use('smog')
            threading.Thread(target=savetheme, args=('smog',)).start()
        
        def changeThemeToWinXPBlue():
            self.style.theme_use('winxpblue')
            threading.Thread(target=savetheme, args=('winxpblue',)).start()
        
        def changeThemeToYaru():
            self.style.theme_use('yaru')
            threading.Thread(target=savetheme, args=('yaru',)).start()
        
        # ---> themes menu
        if self.defaultTheme=='adapta':
            ThemeMenu.add_command(label='Adapta - Default', command=changeThemeToAdapta)
        else:
            ThemeMenu.add_command(label='Adapta', command=changeThemeToAdapta)

        if self.defaultTheme=='arc':
            ThemeMenu.add_command(label='Arc - Default', command=changeThemeToArc)
        else:
            ThemeMenu.add_command(label='Arc', command=changeThemeToArc)
        
        if self.defaultTheme=='aquativo':
            ThemeMenu.add_command(label='Aquativo - Default', command=changeThemeToAquativo)
        else:
            ThemeMenu.add_command(label='Aquativo', command=changeThemeToAquativo)
        
        if self.defaultTheme=='black':
            ThemeMenu.add_command(label='Black - Default', command=changeThemeToBlack)
        else:
            ThemeMenu.add_command(label='Black', command=changeThemeToBlack)
        
        if self.defaultTheme=='blue':
            ThemeMenu.add_command(label='Blue - Default', command=changeThemeToBlue)
        else:
            ThemeMenu.add_command(label='Blue', command=changeThemeToBlue)
        
        if self.defaultTheme=='breeze':
            ThemeMenu.add_command(label='Breeze - Default', command=changeThemeToBreeze)
        else:
            ThemeMenu.add_command(label='Breeze', command=changeThemeToBreeze)
        
        if self.defaultTheme=='clearlooks':
            ThemeMenu.add_command(label='Clearlooks - Default', command=changeThemeToClearlooks)
        else:
            ThemeMenu.add_command(label='Clearlooks', command=changeThemeToClearlooks)
        
        if self.defaultTheme=='elegance':
            ThemeMenu.add_command(label='Elegance - Default', command=changeThemeToElegance)
        else:
            ThemeMenu.add_command(label='Elegance', command=changeThemeToElegance)
        
        if self.defaultTheme=='equilux':
            ThemeMenu.add_command(label='Equilux - Default', command=changeThemeToEquilux)
        else:
            ThemeMenu.add_command(label='Equilux', command=changeThemeToEquilux)
        
        if self.defaultTheme=='keramik':
            ThemeMenu.add_command(label='Keramik - Default', command=changeThemeToKeramik)
        else:
            ThemeMenu.add_command(label='Keramik', command=changeThemeToKeramik)
        
        if self.defaultTheme=='kroc':
            ThemeMenu.add_command(label='Kroc - Default', command=changeThemeToKroc)
        else:
            ThemeMenu.add_command(label='Kroc', command=changeThemeToKroc)
        
        if self.defaultTheme=='plastik':
            ThemeMenu.add_command(label='Plastik - Default', command=changeThemeToPlastik)
        else:
            ThemeMenu.add_command(label='Plastik', command=changeThemeToPlastik)
        
        if self.defaultTheme=='radiance':
            ThemeMenu.add_command(label='Radiance (Ubuntu) - Default', command=changeThemeToRadiance)
        else:
            ThemeMenu.add_command(label='Radiance (Ubuntu)', command=changeThemeToRadiance)
        
        if self.defaultTheme=='smog':
            ThemeMenu.add_command(label='Smog - Default', command=changeThemeToSmog)
        else:
            ThemeMenu.add_command(label='Smog', command=changeThemeToSmog)
        
        if self.defaultTheme=='winxpblue':
            ThemeMenu.add_command(label='Win XP - Default', command=changeThemeToWinXPBlue)
        else:
            ThemeMenu.add_command(label='Win XP', command=changeThemeToWinXPBlue)
        
        if self.defaultTheme=='yaru':
            ThemeMenu.add_command(label='Yaru - Default', command=changeThemeToYaru)
        else:
            ThemeMenu.add_command(label='Yaru', command=changeThemeToYaru)