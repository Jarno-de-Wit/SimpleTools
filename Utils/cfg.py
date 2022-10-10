from tkinter import Tk, filedialog

import pygame
from pygbuttons import Buttons
from .XML import XML

import os
import sys

#DEBUG print statement (comment out second line to print DEBUG(x))
#DEBUG = print
DEBUG = lambda *args, **kwargs: None

backup = False

#Default colour definitions ----------------------------------------------------
grey = (180, 180, 180)
cyan = (0, 63, 63)
dark_blue = (0, 0, 31)
c_accent = (127, 127, 127)
#Other default definitions
help_size = 18

#Just because Tk has to be called before pygame is initiated (on MacOS), it is done in cfg.
root = Tk()
root.withdraw()

#Config loading ----------------------------------------------------------------
try:
    config = XML.XMLFile("config.xml")
except FileNotFoundError:
    config = XML()
except:
    print("Invalid config XML")
    config = XML()

#Load default values for missing keys
for key, default in {
        "ClearOnReload": "true",
        "TrackFolder": "true", #If a folder has been selected, use that as the default instead
        "DefaultFolder": "",
        "Units": "Fuselage Unit",
        }.items():
    config[key] = config.get(key, default)

#If a default folder is given, use that one. Else, select one based on the OS.
if config.get("DefaultFolder", ""):
    SPPath = config["DefaultFolder"]
elif sys.platform == "win32":
    SPPath = os.path.expanduser("~") + "\\AppData\\LocalLow\\Jundroo\\SimplePlanes"
elif sys.platform == "darwin":
    SPPath = os.path.expanduser("~") + "/Library/Application Support/unity.Jundroo.SimplePlanes"
elif sys.platform.beginswith("linux"):
    SPPath = os.getcwd() #TBD
else:
    SPPath = os.getcwd()
    print("Could not recognise OS")
last_path = None

def Unit(value):
    """
    Returns the unit converted from the selected default unit to [m] (the typical unit used in the XML files)
    """
    DEBUG(value)
    if config["Units"] == "Meter":
        return value
    elif config["Units"] == "Fuselage Unit":
        return value / 2
    elif config["Units"] == "Feet":
        return 0.3048006 * value
    else:
        print("You really had to go in and modify the config.xml file, didn't you? Well, now you broke it.")

#Utility functions -------------------------------------------------------------

menu = "Main"
tree = []
focus = False
no_focus = pygame.image.load("Assets/no_focus.png")

def open_file(folder = ""):
    global last_path, SPPath
    file = filedialog.askopenfilename(initialdir = last_path or os.path.join(SPPath, folder), filetypes = (["XML files", ".xml"], ["Other", "*"],))
    if config["TrackFolder"] == "true" and file:
        last_path = os.path.dirname(file)
    return file

def save_file(folder = ""):
    global last_path, SPPath
    file = filedialog.asksaveasfilename(initialdir = last_path or os.path.join(SPPath, folder), filetypes = (["XML files", ".xml"], ["Other", "*"],))
    if config["TrackFolder"] == "true" and file:
        last_path = os.path.dirname(file)
    return file

def back():
    """
    Goes back one step in the menu tree.
    """
    global tree, menu
    if tree:
        menu = tree.pop(-1)
    else:
        global running
        running = False

def enter(name):
    """
    Enters a new menu, and pushes the current menu onto the tree to return to with back().
    """
    global tree, menu
    if not Buttons.get_group(name):
        name = "404"
    tree.append(menu)
    menu = name
    #Clear the newly entered menu (if enabled)
    if config["ClearOnReload"] == "true" and menu not in ["FPanel Coords"]:
        Buttons.Clear(menu)

def Draw():
    """
    Redraws the screen without updating anything
    """
    global resolution, screen, menu
    #Draw the background
    background = pygame.Surface((1, 2))
    pygame.draw.rect(background, cyan, ((0, 0), (1, 1)))
    pygame.draw.rect(background, dark_blue, ((0, 1), (1, 1)))
    screen.blit(pygame.transform.smoothscale(background, resolution), screen.get_rect())

    #Draw the Buttons
    Buttons.Draw(screen, menu)
    #Draw the icon indicating the window isn't focussed (e.g. after file selection)
    if not focus:
        screen.blit(no_focus, (15, 15))
    pygame.display.flip()

