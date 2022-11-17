from pygbuttons import *

from Utils import cfg

from ..Scripts import Revolve

help_text = """Revolves the given part along the axis by n degrees. A rotation without removing the original, thus basically to rotational equivalent of mirroring.

Origin: Any point on the rotation center line. Accepts part selection expressions.\r
Axis: The rotation axis.\r
Number of copies: The amount of new copies which should be created.\r
Angle: The rotation angle, using a left handed coordinate system: If the thumb of your left hand points along the axis, the rotation direction is in the direction of your fingers.\r
 """

def Run():
    buttons["Error"].text_colour = (255, 63, 63)
    buttons["Error"].text = ""
    cfg.Draw()
    success = Revolve.Run(buttons["Input"].value, buttons["Output"].value,
                          buttons["Parts"].value, buttons["Origin"].value,
                          buttons["Axis"].value, buttons["N Copies"].value,
                          buttons["Angle"].value, errout = buttons["Error"])
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
    "Header": Text((120, 50), (400, 50), text = "Revolve", group = ["Revolve", "Revolve Help"], font_size = 40, text_colour = cfg.grey, text_offset = 0, text_align = "center"),
    "Input": TextBox((170, 150), (250, 45), hint = "Input file", group = "Revolve"),
    "Input Menu": Button((425, 150), (45, 45), text = "...", group = "Revolve", functions = {"Click": set_inpf}),
    "Output": TextBox((170, 200), (250, 45), hint = "Output file", group = "Revolve"),
    "Output Menu": Button((425, 200), (45, 45), text = "...", group = "Revolve", functions = {"Click": set_outf}),
    "Parts": TextBox((170, 250), (300, 45), hint = "Parts (id1, id2, ...)", group = "Revolve"),
    "Origin": TextBox((170, 300), (300, 45), hint = "Origin = (0, 0, 0)", group = "Revolve"),
    "Axis": TextBox((170, 350), (300, 45), hint = "Axis, (part id, or 'x, y, z')", group = "Revolve"),
    "N Copies": TextBox((170, 400), (300, 45), hint = "Number of copies", group = "Revolve"),
    "Angle": TextBox((170, 450), (300, 45), hint = "Angle", group = "Revolve"),
    "Run": Button((170, 500), (300, 45), text = "Run", group = "Revolve", functions = {"Click": Run}),
    "Error": Text((120, 550), (400, 90), group = "Revolve", text_colour = (255, 63, 63)),
    "Help": Button((585, 5), (50, 50), text = "?", group = "Revolve", functions = {"Click": (cfg.enter, "Revolve Help")}),
    "Help Text": Text((120, 150), (400, 500), font_size = cfg.help_size, group = "Revolve Help", text = help_text, text_colour = (127, 127, 127))
    }
