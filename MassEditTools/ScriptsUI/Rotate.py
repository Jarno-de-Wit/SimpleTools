from pygbuttons import *

from Utils import cfg

from ..Scripts import Rotate

help_text = """Rotates the given part along the axis by n degrees.

Origin: Any point on the rotation center line. Accepts part selection expressions.

Axis: The rotation axis.

Angle: The rotation angle, using a left handed coordinate system: If the thumb of your left hand points along the axis, the rotation direction is in the direction of your fingers.
 """

def Run():
    buttons["Error"].text_colour = (255, 63, 63)
    buttons["Error"].text = ""
    cfg.Draw()
    success = Rotate.Run(buttons["Input"].value, buttons["Output"].value,
                         buttons["Parts"].value, buttons["Origin"].value,
                         buttons["Axis"].value, buttons["Angle"].value,
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
    "Header": Text((120, 50), (400, 50), text = "Rotate", group = ["Rotate", "Rotate Help"], font_size = 40, text_colour = cfg.grey, text_offset = 0, text_align = "center"),
    "Input": TextBox((170, 150), (250, 45), hint = "Input file", group = "Rotate"),
    "Input Menu": Button((425, 150), (45, 45), text = "...", group = "Rotate", functions = {"Click": set_inpf}),
    "Output": TextBox((170, 200), (250, 45), hint = "Output file", group = "Rotate"),
    "Output Menu": Button((425, 200), (45, 45), text = "...", group = "Rotate", functions = {"Click": set_outf}),
    "Parts": TextBox((170, 250), (300, 45), hint = "Parts (id1, id2, ...)", group = "Rotate"),
    "Origin": TextBox((170, 300), (300, 45), hint = "Origin = (0, 0, 0)", group = "Rotate"),
    "Axis": TextBox((170, 350), (300, 45), hint = "Axis, (part id, or 'x, y, z')", group = "Rotate"),
    "Angle": TextBox((170, 400), (300, 45), hint = "Angle", group = "Rotate"),
    "Run": Button((170, 450), (300, 45), text = "Run", group = "Rotate", functions = {"Click": Run}),
    "Error": Text((120, 500), (400, 115), group = "Rotate", text_colour = (255, 63, 63)),
    "Help": Button((585, 5), (50, 50), text = "?", group = "Rotate", functions = {"Click": (cfg.enter, "Rotate Help")}),
    "Help Text": Text((120, 150), (400, 500), font_size = cfg.help_size, group = "Rotate Help", text = help_text, text_colour = (127, 127, 127))
    }
