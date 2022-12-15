from pygbuttons import *

from Utils import cfg

from ..Scripts import FPanel
from Utils.Vector import Vector

help_text = """Allows for the automatic panelling of 2d shapes.

How to use:
1. Input the coordinates for the shape to be panelled.
2. Select an output file for the output to be saved, and a thickness.
3. Run the script

Shape information:
The shape will automatically be closed. No need to repeat the origin coord.
The final subassembly will consist of n-2 fuselages (n being the amount of coordinates).

Warning:
The edges of the shape should not cross over anywhere. The shape needs a clear "inside" and "outside" to properly generate.
 """

database = [("0", "0"),]# ("1", "0"), ("1", "1"), ("0", "1.5"), ("-1", "0.75")]

#database = {custom coordinates}

"""
Test expression: Uncomment for n-sided "circular" polygon
database = []
n = 6
for i in range(n):
    v = Vector([1, 0]).rotate(i/n * 360)
    database.append((f"{v[0]}",f"{v[1]}"))
"""

def Run():
    global buttons
    if cfg.backup:
        #Make a backup of the database, just in case:
        # To access it, simply open the file in any text editor, and paste the value
        # above after 'database = '
        with open(f"tmp.bak", "w") as f:
            f.write(str(database))
    
    buttons["Error"].text_colour = (255, 63, 63)
    buttons["Error"].Clear()
    buttons["Error"].value = ""
    if cfg.menu == "FPanel Coords":
        cfg.back()
        buttons["Toggle"].value = False

    cfg.Draw()

    success = FPanel.Run(buttons["Output"].value, [", ".join(i) for i in database],
               buttons["Thickness"].value, buttons["Error"])

    if success:
        buttons["Error"].text_colour = (63, 255, 63)
        buttons["Error"].text = "Success"



def Select():
    idx = buttons["Node"].state
    if idx == -1:
        buttons["XPos"].value = buttons["YPos"].value = ""
    else:
        buttons["XPos"].value, buttons["YPos"].value = database[idx]


def Move(direction):
    idx = buttons["Node"].state
    if idx >= 0:
        #The new idx of the current item. If direction = 1, reduce it to 0 since
        # removing the current item will shift all indexes of the following
        # items automatically. idx is also always at least 0, to prevent
        # indexing from the rear of the database.
        new_idx = max(idx + direction, 0)
        buttons["Node"].Del_option(index = idx)
        buttons["Node"].Add_option(f"({database[idx][0]}, {database[idx][1]})", index = new_idx, set_to = True)
        database.insert(new_idx, database.pop(idx))

def Add():
    idx = buttons["Node"].state + 1
    buttons["Node"].Add_option("(, )", index = idx, set_to = True)
    database.insert(idx, ("", ""))
    buttons["XPos"].value = buttons["YPos"].value = ""

def Del():
    nd = buttons["Node"]
    print(nd.options)
    idx = buttons["Node"].state
    if idx >= 0:
        database.pop(idx)
        buttons["Node"].Del_option(index = idx)
        buttons["Node"].state = idx - 1
    Select()


def Update():
    idx = buttons["Node"].state
    if idx >= 0:
        database[buttons["Node"].state] = (buttons["XPos"].value, buttons["YPos"].value)
        #buttons["Node"].Edit_option(buttons["Node"].state, value = f"({database[idx][0]}, {database[idx][1]})")
        buttons["Node"].button_list[idx].text = f"({database[idx][0]}, {database[idx][1]})"
        buttons["Node"].state += 0

def set_outf():
    global buttons
    file = cfg.save_file("SubAssemblies")
    if file:
        buttons["Output"].value = file

buttons = {
    "Header": Text((110, 50), (420, 50), text = "Shaped Panel", group = ["FPanel", "FPanel Coords", "FPanel Help"], font_size = 40, text_colour = cfg.grey, text_offset = 0, text_align = "center"),
    "Toggle": Button((170, 150), (300, 45), mode = "Toggle", text = "Edit Coords", group = ["FPanel", "FPanel Coords"], functions = {"Click": (cfg.enter, "FPanel Coords"), "Release": cfg.back}),
    #Main menu buttons
    "Output": TextBox((170, 200), (250, 45), hint = "Output file", group = "FPanel"),
    "Output Menu": Button((425, 200), (45, 45), text = "...", group = "FPanel", functions = {"Click": set_outf}),
    "Thickness": TextBox((170, 250), (300, 45), hint = "Thickness", group = "FPanel"),
    "Error": Text((120, 300), (400, 250), group = "FPanel", text_colour = (255, 63, 63), scroll_bar = 1),
    #Coord editing buttons
    "Node": DropdownBox((170, 200), (300, 45), options = ["(0, 0)"], display_length = 4.5, scroll_bar = 2, hint = "Node", group = "FPanel Coords", functions = {"Deselect": Select}),
    "Add": Button((170, 250), (45, 45), text = "+", group = "FPanel Coords", functions = {"Click": Add}),
    "Del": Button((220, 250), (45, 45), text = "-", group = "FPanel Coords", functions = {"Click": Del}),
    "XMirror": Button((375, 250), (45, 45), text = "><", group = "FPanel Coords"),
    "YMirror": Button((425, 250), (45, 45), text = "^v", group = "FPanel Coords"),
    "Up": Button((270, 250), (45, 45), text = "^", group = "FPanel Coords", functions = {"Click": (Move, -1)}),
    "Down": Button((325, 250), (45, 45), text = "v", group = "FPanel Coords", functions = {"Click": (Move, 1)}),
    "XPos": TextBox((170, 300), (145, 45), hint = "X Pos", group = "FPanel Coords", functions = {"Type": Update}),
    "YPos": TextBox((325, 300), (145, 45), hint = "Y Pos", group = "FPanel Coords", functions = {"Type": Update}),
#    "Preview": Button((170, 350), (300, 200), group = "FPanel Coords"),
    #Other buttons
    "Run": Button((170, 555), (300, 45), text = "Run", group = ["FPanel", "FPanel Coords"], functions = {"Click": Run}),
    "Help": Button((585, 5), (50, 50), text = "?", group = ["FPanel", "FPanel Coords"], functions = {"Click": (cfg.enter, "FPanel Help")}),
    "Help Text": Text((95, 125), (450, 475), font_size = cfg.help_size, text = help_text, group = "FPanel Help", text_colour = cfg.grey),
    "Back": Button((220, 655), (200, 30), text = "Back", group = ["FPanel", "FPanel Coords", "FPanel Help"], functions = {"Click": cfg.back}),
           }

for point in database[1:]:
    buttons["Node"].Add_option(f"({round(float(point[0]), 3)}, {round(float(point[1]), 3)})")
buttons["Node"].state = 0
Select()

