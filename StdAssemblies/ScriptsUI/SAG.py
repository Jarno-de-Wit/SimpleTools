from pygbuttons import *

from Utils import cfg

help_text = """This menu contains a multitude of "standard" assemblies one might need in their builds

Curve: A partial torroid made from multiple straight fuselage pieces

Shaped Panel: A flat plane, following the shape specified, made from multiple fuselage pieces
 """

buttons = {
    "Header": Text((110, 50), (420, 50), text = "Standard Assemblies", group = ["SAG", "SAG Help"], font_size = 40, text_colour = cfg.grey, text_offset = 0, text_align = "center"),
    "Curve": Button((170, 200), (300, 45), text = "Curve Creator", group = "SAG", functions = {"Click": (cfg.enter, "Curve")}),
    "Shaped Panel": Button((170, 250), (300, 45), text = "Shaped Panel", group = "SAG", functions = {"Click": (cfg.enter, "FPanel")}),

    "Ideas": Text((170, 350), (300, 500), text = "Have any ideas for more standard assemblies? Let me know!\n ", group = "SAG", text_colour = (63, 255, 63), text_align = "Top"),
    "Help": Button((585, 5), (50, 50), text = "?", group = "SAG", functions = {"Click": (cfg.enter, "SAG Help")}),
    "Help Text": Text((95, 150), (450, 425), font_size = cfg.help_size, text = help_text, group = "SAG Help", text_colour = cfg.grey),
    "Back": Button((220, 655), (200, 30), text = "Back", group = ["SAG", "SAG Help"], functions = {"Click": cfg.back}),
           }

