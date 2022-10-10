from pygbuttons import *

from Utils import cfg

from ..Scripts import ME

help_text = """A mass part property editor.

Parts: The selection expression for the parts which should be edited.

Path: The path / name of the property to be edited. E.G. 'partType' or 'InputController/input'

Operation: The operation to be performed on the value. See info.txt for more information.

Value: The new value which the path should be set to, which should be appended, ...

Default Value: The initial value which should be used if the value does not yet exist for a part.
 """

def Run():
    buttons["Error"].text_colour = (255, 63, 63)
    buttons["Error"].text = ""
    cfg.Draw()
    success = ME.Run(buttons["Input"].value, buttons["Output"].value,
                     buttons["Parts"].value, buttons["Path"].value,
                     buttons["Operation"].value, buttons["Value"].value,
                     buttons["Default"].value, errout = buttons["Error"])
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
    "Header": Text((120, 50), (400, 50), text = "Mass Editor", group = ["ME", "ME Help"], font_size = 40, text_colour = cfg.grey, text_offset = 0, text_align = "center"),
    "Input": TextBox((170, 150), (250, 45), hint = "Input file", group = "ME"),
    "Input Menu": Button((425, 150), (45, 45), text = "...", group = "ME", functions = {"Click": set_inpf}),
    "Output": TextBox((170, 200), (250, 45), hint = "Output file", group = "ME"),
    "Output Menu": Button((425, 200), (45, 45), text = "...", group = "ME", functions = {"Click": set_outf}),
    "Parts": TextBox((170, 250), (300, 45), hint = "Parts (id1, id2, ...)", group = "ME"),
    "Path": TextBox((170, 300), (300, 45), hint = "Path / Value name", group = "ME"),
    "Operation": DropdownBox((170, 350), (300, 45), ["Set", "+=", "-=", "*=", "/=", "Append", "Prepend"], scroll_bar = 2, display_length = 4.5, hint = "Edit mode", group = "ME"),
    "Value": TextBox((170, 400), (300, 45), hint = "Value", group = "ME"),
    "Default": TextBox((170, 450), (300, 45), hint = "Default Value", group = "ME"),
    "Run": Button((170, 500), (300, 45), text = "Run", group = "ME", functions = {"Click": Run}),
    "Error": Text((120, 550), (400, 95), group = "ME", text_colour = (255, 63, 63)),
    "Help": Button((585, 5), (50, 50), text = "?", group = "ME", functions = {"Click": (cfg.enter, "ME Help")}),
    "Help Text": Text((120, 150), (400, 500), font_size = cfg.help_size, group = "ME Help", text = help_text, text_colour = (127, 127, 127))
    }
