from pygbuttons import *

from Utils import cfg

from ..Scripts import Scale

help_text = """Scales the selected parts with the given factor.

Origin: The location from which the parts should be scaled. Relevant if not all parts in a craft are scaled.

Scaling factor: The multiplication factor with which the parts should be scaled.

Scale Mode: How the part scaling should take place. Allows for positional scaling, and part size scaling, or both.
 """

def Run():
    buttons["Error"].text_colour = (255, 63, 63)
    buttons["Error"].text = ""
    cfg.Draw()
    success = Scale.Run(buttons["Input"].value, buttons["Output"].value,
                        buttons["Parts"].value, buttons["Origin"].value,
                        buttons["Scale"].value, buttons["Scale Mode"].value,
                        errout = buttons["Error"])
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
    "Header": Text((120, 50), (400, 50), text = "Scale", group = ["Scale", "Scale Help"], font_size = 40, text_colour = cfg.grey, text_offset = 0, text_align = "center"),
    "Input": TextBox((170, 150), (250, 45), hint = "Input file", group = "Scale"),
    "Input Menu": Button((425, 150), (45, 45), text = "...", group = "Scale", functions = {"Click": set_inpf}),
    "Output": TextBox((170, 200), (250, 45), hint = "Output file", group = "Scale"),
    "Output Menu": Button((425, 200), (45, 45), text = "...", group = "Scale", functions = {"Click": set_outf}),
    "Parts": TextBox((170, 250), (300, 45), hint = "Parts (id1, id2, ...)", group = "Scale"),
    "Origin": TextBox((170, 300), (300, 45), hint = "Origin = (0, 0, 0)", group = "Scale"),
    "Scale": TextBox((170, 350), (300, 45), hint = "Scaling factor", group = "Scale"),
    "Scale Mode": DropdownBox((170, 400), (300, 45), ["Part Size", "Position", "Size + Position"], group = "Scale", hint = "Scale mode"),
    "Run": Button((170, 450), (300, 45), text = "Run", group = "Scale", functions = {"Click": Run}),
    "Error": Text((120, 500), (400, 115), group = "Scale", text_colour = (255, 63, 63)),
    "Help": Button((585, 5), (50, 50), text = "?", group = "Scale", functions = {"Click": (cfg.enter, "Scale Help")}),
    "Help Text": Text((120, 150), (400, 500), font_size = cfg.help_size, group = "Scale Help", text = help_text, text_colour = (127, 127, 127))
    }
