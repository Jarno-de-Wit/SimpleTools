from pygbuttons import *
from . import cfg

buttons = {
    "Header": Text((120, 50), (300, 50), text = "Error: 404", group = "404", font_size = 41, text_colour = cfg.grey, text_offset = 0, text_align = "center"),
    "Err": Text((95, 150), (450, 380), text = "This page does not exist yet. I am sorry for the inconvenience.", group = "404", text_colour = cfg.grey),
    "Back": Button((220, 655), (200, 30), text = "Back", group = "404", functions = {"Click": cfg.back}),
    }
