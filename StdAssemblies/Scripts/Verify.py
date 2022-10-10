"""
A simple input verification script. A stripped down version from the one in MassEditTools.
"""
import os
import sys

from Utils.Vector import Vector
from Utils.Vect3d import Rot_to_vect


errors = False
__errout = sys.stderr


def Err(msg = None):
    global errors, __errout
    if msg is not None and __errout is not None:
        print(msg, file = __errout)
    errors = True
    return None

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

def coord3d(value):
    ...


def coord2d(value):
    try:
        coord = Vector.from_css(value)
        if len(coord) != 2:
            return Err("Incorrect coordinate dimension")
        return coord
    except TypeError:
        return Err("Invalid coordinate")
    ...

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

def Verify(out_file = None, pos2d = None, pos3d = None, int_ = None, float_ = None, errout = sys.stderr):
    """
    A wrapper function to batch verify the most common values, including those which depend on the craft file.
    """
    global errors, __errout
    __errout = errout
    errors = False
    out = []

    if output_file:
        out.append(output_file(out_file))

    if pos2d is not None:
        if isinstance(pos2d, str):
            pos2d = [pos2d]
        for position in pos2d:
            out.append(coord2d(position))

    if pos3d is not None:
        if isinstance(pos3d, str):
            pos3d = [pos3d]
        for position in pos3d:
            out.append(coord3d(position))

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

