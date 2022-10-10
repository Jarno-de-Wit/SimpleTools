"""
Revolves a part / multiple parts around an axis, creating new copies of the part
at user defined angles.
"""

#Import standard python libraries
import math
import os
import sys

from Utils import cfg

#Import custom python libraries
from Utils.Vector import Vector
from Utils.Vect3d import Rot_to_vect, Vect_to_rot

from .Verify import Verify
from Utils import SimpleUtils as SP

def Run(input_file, output_file, ids, origin, normal, errout = sys.stderr):
    """
    Verifies all inputs, and runs the script if all inputs are valid.
    """
    errors, craft, output_file, ids, origin, normal = \
            Verify(input_file, output_file, ids, origin, normal, errout = errout)

    if not errors: #If all data was input correctly:
        return Flip(craft, output_file, ids, origin, normal, errout)
    return False


def Flip(craft, output_file, ids, origin, normal, errout = sys.stderr):
    """
    Scales multiple parts relative to a given point.
    """
    parts = craft.find("Parts")
    normal = normal.unit

    for id_ in ids:
        part = parts.get_filtered("id", str(id_))
        part = Flip(part)
        #Calculate the new part position
        pos = Vector.from_css(part["position"])
        pos -= 2 * (pos - origin).projection(normal)
        part["position"] = pos.css()
        #Turn the rotation into Vectors, then rotate those vectors
        x, y, z = Rot_to_vect(Vector.from_css(part["rotation"]))
        #Note: During the flipping of the rotation, only two Vectors can be kept
        # consistent. The third Vector instead has to be accounted for by
        # the parts geometry. In this case, this is chosen to be the X-vector
        # (sideways) because this is the easiest to flip. (Most parts are
        # symmetric on this axis anyway).
        z -= 2 * z.projection(normal)
        y -= 2 * y.projection(normal)
        x -= 2 * y.projection(normal)
        #Calculate the new rotation, and save it
        # For wheels (which are not always symmetric along X, keep X consistent,
        # and instead allow z (their symmetry axis) to be free
        if "Wheel" in part["partType"]:
            part["rotation"] = Vect_to_rot(x, y, None).css()
        #Wings have a similar issue, except for having their symmetry axis in the
        # Y direction.
        elif "Wing" in part["partType"]:
            part["rotation"] = Vect_to_rot(x, None, z).css()
        else:
            part["rotation"] = Vect_to_rot(None, y, z).css()

    #Save the final craft to the given output file
    craft.write(output_file)
    return True

def Flip_part(part):
    """
    Changes a parts properties such that it is a mirror of the original part.
    """
    if "fuselage" in part["partType"]:
        corners = Vector.from_css(part["Fuselage.State"]["cornerTypes"])
        corners = Vector(list(reversed(corners[:4])) + list(reversed(corners[4:]))).css()
        part["Fuselage.State"]["cornerTypes"] = corners
    elif part["partType"] == "Wheel-Resizable-1":
        #Change the driving direction to account for the changed "forward"
        part["ResizableWheel.State"]["direction"] = "Reversed" if part["ResizableWheel.State"]["direction"] == "Normal" else "Normal"
    elif "Rotator" in part["partType"]:
        #Change the rotation direction to account for the flipped world
        part["InputController.State"]["invert"] = "false" if part["InputController.State"]["invert"] == "true" else "true"
    elif "Wing" in part["partType"]:
        #Flip the zero lift AoA of the wing to account for the changed "upwards"
        part["Wing.State"]["inverted"] = "false" if part["Wing.State"]["inverted"] == "true" else "true"
    return part
