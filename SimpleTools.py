import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = ""
import pygame

from pygbuttons import *

import MassEditTools.ScriptsUI
import StdAssemblies.ScriptsUI
from Utils import cfg, Error404, Settings
import timeit
from Utils.XML import XML


cyan = (0, 63, 63)
dark_blue = (0, 0, 31)
grey = (180, 180, 180)

help_text = """Welcome to SimpleTools, a program created to help perform simple tasks for the game SimplePlanes
 """
credit_text = """PygButtons: Me
SP Help: Funky Trees Discord Server
 """


def Main():
    """
    globals:
    running: Defines whether the program should continue running
    resolution: The resolution of the display
    """
    cfg.running = True
    cfg.resolution = (640, 720)
    Buttons.framerate = 30
    cfg.menu = "Main"
    pygame.init()
    pygame.key.set_repeat(500, 50)
    cfg.screen = pygame.display.set_mode(cfg.resolution, pygame.RESIZABLE)
    pygame.display.set_caption("SimpleTools")
    cfg.clock = pygame.time.Clock()
    #buttons = Make_buttons()

    while cfg.running:
        Handle_input()
        cfg.Draw()
        cfg.clock.tick(Buttons.framerate)

def Handle_input():
    global q
    for event in pygame.event.get():
        if False and event.type == pygame.MOUSEBUTTONDOWN and event.key > 2:
            q = event
#            print("caught")
        #Let the Buttons process the event first
        Buttons.Event(event, cfg.menu)
        #If any button used the event, move on
        if Buttons.input_processed:
            continue

        #Perform manual processing where required
        if event.type == pygame.QUIT:
            cfg.running = False
            return
        elif event.type == pygame.VIDEORESIZE:
            set_res(event.size)
        elif event.type == pygame.WINDOWFOCUSGAINED:
            cfg.focus = True
        elif event.type == pygame.WINDOWFOCUSLOST:
            cfg.focus = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cfg.back() #Take one step back in the menu depth
    Buttons.Update(cfg.menu)

def init():
    global buttons
    buttons = {
        "Header": Text((120, 50), (400, 50), text = "SimpleTools", group = ["Main", "Main Help", "Credits"], font_size = 40, text_colour = grey, text_offset = 0, text_align = "center"),
        "MET": Button((170, 200), (300, 45), text = "Mass Edit Tools", group = "Main", functions = {"Click": (cfg.enter, "MET")}),
        "SAG": Button((170, 250), (300, 45), text = "Standard Assemblies", group = "Main", functions = {"Click": (cfg.enter, "SAG")}),
#        "FT":  Button((170, 300), (300, 45), text = "Funky Trees", group = "Main", functions = {"Click": (cfg.enter, "FT")}),
#        "MLE": Button((170, 350), (300, 45), text = "Map Location Editor", group = "Main", functions = {"Click": (cfg.enter, "MLE")}),
        "Settings": Button((220, 570), (200, 35), text = "Settings", group = "Main", functions = {"Click": Settings.load}),# text_offset = 0),
        "Credits": Button((220, 620), (200, 30), text = "Credits", group = "Main", functions = {"Click": (cfg.enter, "Credits")}),
        "Quit": Button((220, 655), (200, 30), text = "Quit", group = "Main", functions = {"Click": cfg.back}),
        "Help": Button((585, 5), (50, 50), text = "?", group = "Main", functions = {"Click": (cfg.enter, "Main Help")}),
        "Help Text": Text((95, 150), (450, 380), font_size = cfg.help_size, text = help_text, group = "Main Help", text_colour = grey),
        "Credit Text": Text((95, 150), (450, 380), text = credit_text, group = "Credits", text_colour = grey),
        "Credit Subtitle": Text((120, 95), (400, 40), text = "Credits", group = "Credits", font_size = 25, text_offset = 0, text_colour = grey),#, align = "center"),
        "Back": Button((220, 655), (200, 30), text = "Back", group = ["Main Help", "Credits"], functions = {"Click": cfg.back}),
        }
    for button in Buttons.list_all:
        button.Add_to_group("Scaled")
    return buttons

def set_res(res):
    cfg.resolution = res
    Buttons.Scale(min(res[0] / 640, res[1] / 720), "Scaled", False)


if __name__ == "__main__":
    try:
        buttons = init()
        Main()
    finally:
        pygame.quit()
        pass
