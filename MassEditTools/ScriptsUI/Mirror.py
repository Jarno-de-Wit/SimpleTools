from pygbuttons import *

from Utils import cfg

from ..Scripts import Mirror

help_text = """Mirrors the given parts over the given plane.

Origin: The origin point of the plane. Can be any point which lies within the mirroring plane.\r
Normal Vector: The vector / line which has a 90 degree angle to the mirroring plane.\r
 """

def Run():
    buttons["Error"].text_colour = (255, 63, 63)
    buttons["Error"].text = ""
    cfg.Draw()
    success = Mirror.Run(buttons["Input"].value, buttons["Output"].value,
                        buttons["Parts"].value, buttons["Origin"].value,
                        buttons["Normal"].value, errout = buttons["Error"])
    if success:
        buttons["Error"].text_colour = (63, 255, 63)
        buttons["Error"].text = "Success"

def set_inpf():
    global buttons
    file = cfg.open_file("AircraftDesigns")
    if file:
        buttons["Input"].value = file

def set_outf():
    global buttons
    file = cfg.save_file("AircraftDesigns")
    if file:
        buttons["Output"].value = file


buttons = {
    "Header": Text((120, 50), (400, 50), text = "Mirror", group = ["Mirror", "Mirror Help"], font_size = 40, text_colour = cfg.grey, text_offset = 0, text_align = "center"),
    "Input": TextBox((170, 150), (250, 45), hint = "Input file", group = "Mirror"),
    "Input Menu": Button((425, 150), (45, 45), text = "...", group = "Mirror", functions = {"Click": set_inpf}),
    "Output": TextBox((170, 200), (250, 45), hint = "Output file", group = "Mirror"),
    "Output Menu": Button((425, 200), (45, 45), text = "...", group = "Mirror", functions = {"Click": set_outf}),
    "Parts": TextBox((170, 250), (300, 45), hint = "Parts (id1, id2, ...)", group = "Mirror"),
    "Origin": TextBox((170, 300), (300, 45), hint = "Origin = (0, 0, 0)", group = "Mirror"),
    "Normal": TextBox((170, 350), (300, 45), hint = "Normal Vector", group = "Mirror"),
    "Run": Button((170, 400), (300, 45), text = "Run", group = "Mirror", functions = {"Click": Run}),
    "Error": Text((120, 450), (400, 115), group = "Mirror", text_colour = (255, 63, 63)),
    "Help": Button((585, 5), (50, 50), text = "?", group = "Mirror", functions = {"Click": (cfg.enter, "Mirror Help")}),
    "Help Text": Text((120, 150), (400, 500), font_size = cfg.help_size, group = "Mirror Help", text = help_text, text_colour = (127, 127, 127))
    }
