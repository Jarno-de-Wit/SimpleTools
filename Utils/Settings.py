from pygbuttons import *

from Utils import cfg

help_text = """This menu contains the settings for SimpleTools

Clear on Reload: Whether the entered values for any of the tools should be cleared when re-entering the menu.

Track Folder: Whether the file path should follow the last used folder (or always go to the Default Folder if disabled).

Default Folder: The folder in which the file dialog will open when selecting a file. If empty, defaults to the standard install directory.

Units: The unit used when entering size / distance values. Note: Does NOT affect part selection expressions.
 """

def save():
    #Set all boolean Settings
    for name in ["ClearOnReload", "TrackFolder"]:
        cfg.config[name] = "true" if buttons[name].value else "false"
    #Set all string Settings
    for name in ["DefaultFolder"]:
        cfg.config[name] = buttons[name].value
    #Set all multiple choice Settings
    for name in []:
        cfg.config[name] = buttons[name].value
    #Save the config XML to the file
    cfg.config.write("config.xml")
    cfg.back()

def load():
    cfg.enter("Settings")
    #Loads settings from cfg into Buttons.
    #Required every time to prevent desync when exited without saving
    buttons["ClearOnReload"].value = cfg.config["ClearOnReload"] == "true"
    buttons["TrackFolder"].value = cfg.config["TrackFolder"] == "true"
    buttons["DefaultFolder"].value = cfg.config["DefaultFolder"]
    try:
        buttons["Units"].value = cfg.config["Units"]
    except ValueError:
        buttons["Units"].state = -1

buttons = {
    "Header": Text((110, 50), (420, 50), text = "Settings", group = ["Settings", "Settings Help"], font_size = 40, text_colour = cfg.grey, text_offset = 0, text_align = "center"),
    "ClearOnReload": Button((170, 200), (35, 35), group = "Settings", mode = "Toggle", accent_background = cfg.c_accent),
    "ClearOnReloadText": Text((220, 200), (250, 35), text = "Clear on Reload", text_colour = cfg.grey, group = "Settings", text_align = "Left"),
    "TrackFolder": Button((170, 240), (35, 35), group = "Settings", mode = "Toggle", accent_background = cfg.c_accent),
    "TrackFolderText": Text((220, 240), (250, 35), text = "Track Last Folder", text_colour = cfg.grey, group = "Settings", text_align = "Left"),
    "DefaultFolder": TextBox((170, 280), (300, 40), hint = "Default Folder", group = "Settings"),
    "Units": DropdownBox((170, 325), (300, 40), hint = "Units", options = ["Fuselage Unit", "Meter", "Feet"], group = "Settings"),
    "Help": Button((585, 5), (50, 50), text = "?", group = "Settings", functions = {"Click": (cfg.enter, "Settings Help")}),
    "Help Text": Text((95, 150), (450, 425), font_size = cfg.help_size, text = help_text, group = "Settings Help", text_colour = cfg.grey, scroll_bar = 1),
    "SaveExit": Button((220, 620), (200, 30), text = "Save + Back", group = "Settings", functions = {"Click": save}),
    "Back": Button((220, 655), (200, 30), text = "Back", group = ["Settings", "Settings Help"], functions = {"Click": cfg.back}),
    }

