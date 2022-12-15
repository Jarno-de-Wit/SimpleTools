from pygbuttons import *

from Utils import cfg

help_text = """This menu contains a multitude of tools to perform mass editing of parts, copying of parts, or moving of parts.

Mass Editor: Provides an interface to change part properties in mass.\r
Scale: Allows you to change the scale of (a part of) the craft.\r
Rotate: Allows (a subsection of) a craft to be rotated around a specified axis.\r
Revolve: Allows for the creation of copies of (a part of) the craft, each copy being rotated by n degrees.\r
Flip: Flip (a section of) the craft about a given plane.\r
Mirror: Creates a new copy of (a part of) the craft, flipped around a given plane.\r
 """

buttons = {
    "Header": Text((120, 50), (400, 50), text = "Mass Edit Tools", group = ["MET", "MET Help"], font_size = 40, text_colour = cfg.grey, text_offset = 0, text_align = "center"),
    "ME": Button((170, 200), (300, 45), text = "Mass Editor", group = "MET", functions = {"Click": (cfg.enter, "ME")}),
    "Scale": Button((170, 250), (300, 45), text = "Scale", group = "MET", functions = {"Click": (cfg.enter, "Scale")}),
    "Rotate":  Button((170, 300), (300, 45), text = "Rotate", group = "MET", functions = {"Click": (cfg.enter, "Rotate")}),
    "Revolve": Button((170, 350), (300, 45), text = "Revolve", group = "MET", functions = {"Click": (cfg.enter, "Revolve")}),
    "Flip": Button((170, 400), (300, 45), text = "Flip", group = "MET", functions = {"Click": (cfg.enter, "Flip")}),
    "Mirror": Button((170, 450), (300, 45), text = "Mirror", group = "MET", functions = {"Click": (cfg.enter, "Mirror")}),
    "Help": Button((585, 5), (50, 50), text = "?", group = "MET", functions = {"Click": (cfg.enter, "MET Help")}),
    "Help Text": Text((95, 150), (450, 425), font_size = cfg.help_size, text = help_text, group = "MET Help", text_colour = cfg.grey),
    "Back": Button((220, 655), (200, 30), text = "Back", group = ["MET", "MET Help", "ME", "ME Help", "Rotate", "Rotate Help", "Revolve", "Revolve Help", "Scale", "Scale Help", "Flip", "Flip Help", "Mirror", "Mirror Help"], functions = {"Click": cfg.back}),
    }
