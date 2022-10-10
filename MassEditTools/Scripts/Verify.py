import os
import sys
#from Utils.XML import XML
#from Utils.Vector import Vector
from Utils.XML import XML
from Utils.Vector import Vector
from Utils.Vect3d import Rot_to_vect
from .IDParse import parse, Part, init, ParseError

errors = False
__errout = sys.stderr

def Err(msg = None):
    global errors, __errout
    if msg is not None and __errout is not None:
        print(msg, file = __errout)
    errors = True
    return None

def input_file(path, errout = sys.stderr):
    """
    Verifies the input craft file, and loads it
    """
    if os.path.exists(path):
        craft = XML.XMLFile(path)
        if not (isinstance(craft.find("Parts"), XML) and isinstance(craft.find("Connections"), XML) and isinstance(craft.find("Theme"), XML)):
            return Err("Invalid craft XML file")
        return craft
    else:
        return Err(f"Could not find selected input file")

def output_file(path):
    """
    Verifies the path of the output file.
    """
    if not os.path.basename(path):
        return Err("Missing output file name")
    #Verify if the target folder exists. If not, we can't make a file there either.
    #Separate test for empty str dirname, because os.path.isdir assumes returns
    # False for that, even though the current directory definitely exists.
    elif os.path.isdir(os.path.dirname(path)) or not os.path.dirname(path):
        return path
    else:
        return Err(f"Could not create selected output file due to missing folder structure")

def Pos(value):
    """
    Verifies a string as input in a coords section, and returns the corresponding coords as a Vector
    """
    value = value.strip(" \t")
    #Option 1: An empty coords section defaults to the origin
    if not value:
        return Vector([0, 0, 0])
    #Option 2: An actual Vector
    try:
        pos = Vector.from_css(value)
        if len(pos) == 3:
            return pos
    except: pass
    #Option 3: An expression for the part id is given
    ids = parse(value, True)
    if ids is None:
        return Err() #Silent Err (already Err in parse)
    if len(ids) != 1:
        return Err(f"Part selection criteria for coordinates {'not strict enough' if ids else 'too strict'}")
    return Vector.from_css(Part(ids[0])["position"])

def __facing(part):
    """
    Returns the "facing" Vector of the given part
    """
    if isinstance(part, XML):
        return Rot_to_vect(Vector.from_css(part["rotation"]))[2]
    else:
        return Err("No part with given ID found to take 'facing' direction from")

def Axis(value):
    """
    Verifies a string as input in an axis section, and returns the corresponding axis as a Vector
    """
    global errors
    #Option 1: An empty axis section defaults to positive Z axis (forwards)
    if not value.strip(" \t"):
        return Vector([0, 0, 1])
    elif value.lower() in ["x", "y", "z"]:
        value = value.lower()
        return Vector([int(value == "x"), int(value == "y"), int(value == "z")])
    #Option 2: An actual Vector
    try:
        axis = Vector.from_css(value)
        if len(axis) == 3:
            return axis
    except: pass
    #Option 3: An expression for the part id is given
    ids = parse(value, True)
    if ids is None:
        return Err() #Silent Err (already Err in parse)
    if len(ids) != 1:
        return Err(f"Part selection criteria for axis {'not strict enough' if ids else 'too strict'}")
    return __facing(Part(ids[0]))

def Int(value):
    try:
        return int(value)
    except ValueError:
        return Err("Invalid integer number")

def Number(value):
    try:
        return float(value)
    except ValueError:
        return Err("Invalid number")

def Verify(inp_file = None, out_file = None, parts = None, pos = None, axis = None, int_ = None, float_ = None, errout = sys.stderr):
    """
    A wrapper function to batch verify the most common values, including those which depend on the craft file.
    """
    global errors, __errout
    __errout = errout
    errors = False
    out = []
    craft = None

    if input_file is not None:
        craft = input_file(inp_file)
        out.append(craft)
    #Setup the IDParse module
    init(craft, errout)

    if output_file:
        out.append(output_file(out_file))
    if parts is not None:
        if craft is not None: #If the craft file was opened sucessfully
            try:
                out.append(parse(parts))
            except ParseError as e:
                out.append(Err(e.args[0] if e.args else None))
        else:
            out.append(Err())

    if pos is not None:
        if isinstance(pos, str):
            pos = [pos]
        for position in pos:
            out.append(Pos(position))

    if axis is not None:
        if isinstance(axis, str): #Allow a single passed in axis field to be handled properly, as well as multiple passed in axis fields
            axis = [axis]
        for ax in axis:
            out.append(Axis(ax))

    if int_ is not None:
        if isinstance(int_, str):
            int_ = [int_]
        for i in int_:
            out.append(Int(i))

    if float_ is not None:
        if isinstance(float_, str):
            float_ = [float_]
        for i in float_:
            out.append(Number(i))
        
    return errors, *out
