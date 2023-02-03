from pygbuttons import *

from Utils import cfg

from ..Scripts import Curve

help_text = """Creates a round shape by placing n fuselage pieces one after another, each shifted by some angle.

Angle: The per-segment angle offset.\r
Radius: The radius to the centerline of the fuselage (at their closest approach point).\r
Thickness: The diameter of the fuselage pieces used.\r
Truncate edges: Whether the two edge positioned fuselage pieces should be 'truncated' / cut to not exceed the centerline. Useful when chaining multiple curves together.\r
Rounded edges: Whether the connection of the fuselages should use 'balls' to create proper rounding. This can especially help make low fuselage count curves look smoother.\n
Radius and Thickness both support ranges. Use a-b for a linear range, or a~b for a cosine shaped range.
 """

def Run():
    buttons["Error"].text_colour = (255, 63, 63)
    buttons["Error"].Clear()
    buttons["Error"].text = ""
    cfg.Draw()
    success = Curve.Run(buttons["Output"].value, buttons["Angle"].value,
                         buttons["Radius"].value, buttons["Thickness"].value,
                         buttons["Nr segments"].value, buttons["Truncate"].value,
                         buttons["Rounded"].value, errout = buttons["Error"])
    if success:
        buttons["Error"].text_colour = (63, 255, 63)
        buttons["Error"].text = "Success"

def set_outf():
    global buttons
    file = cfg.save_file("SubAssemblies")
    if file:
        buttons["Output"].value = file


buttons = {
    "Header": Text((120, 50), (400, 50), text = "Curve", group = ["Curve", "Curve Help"], font_size = 40, text_colour = cfg.grey, text_offset = 0, text_align = "center"),
    "Output": TextBox((170, 150), (250, 45), hint = "Output file", group = "Curve"),
    "Output Menu": Button((425, 150), (45, 45), text = "...", group = "Curve", functions = {"Click": set_outf}),
    "Angle": TextBox((170, 200), (300, 45), hint = "Angle (per segment)", group = "Curve"),
    "Radius": TextBox((170, 250), (300, 45), hint = "Radius", group = "Curve"),
    "Thickness": TextBox((170, 300), (300, 45), hint = "Thickness", group = "Curve"),
    "Nr segments": TextBox((170, 350), (300, 45), hint = "Nr of segments", group = "Curve"),
    "Truncate": Button((170, 400), (45, 45), group = "Curve", mode = "Toggle", accent_background = cfg.c_accent),
    "Truncate Text": Text((230, 400), (1240, 35), text = "Truncate edges", text_colour = cfg.grey, group = "Curve", text_align = "Left"),
    "Rounded": Button((170, 450), (45, 45), group = "Curve", mode = "Toggle", accent_background = cfg.c_accent),
    "Rounded Text": Text((230, 450), (1240, 35), text = "Round corners", text_colour = cfg.grey, group = "Curve", text_align = "Left"),
    "Run": Button((170, 500), (300, 45), text = "Run", group = "Curve", functions = {"Click": Run}),
    "Error": Text((120, 550), (400, 100), group = "Curve", text_colour = (255, 63, 63), scroll_bar = 1),
    "Help": Button((585, 5), (50, 50), text = "?", group = "Curve", functions = {"Click": (cfg.enter, "Curve Help")}),
    "Help Text": Text((120, 150), (400, 500), font_size = cfg.help_size, group = "Curve Help", text = help_text, text_colour = (127, 127, 127)),
    "Back": Button((220, 655), (200, 30), text = "Back", group = ["Curve", "Curve Help"], functions = {"Click": cfg.back}),
    }
