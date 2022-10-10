"""
Rotates a part / multiple parts around an axis. Does not create any new parts.
"""

#Import standard python libraries
import math
import os
import sys

from Utils import cfg

#Import custom python libraries
from Utils.Vector import Vector
from Utils.Vect3d import Rot_to_vect, Vect_to_rot
from Utils.Vect3d import Rotate as Rot3d

from .Verify import Verify



def Run(input_file, output_file, ids, origin, axis, angle, errout = sys.stderr):
    """
    Verifies all inputs, and runs the script if all inputs are valid.
    """
    errors, craft, output_file, ids, origin, axis, angle = \
            Verify(input_file, output_file, ids, origin, axis, float_ = angle, errout = errout)

    if not errors: #If all data was input correctly:
        return Rotate(craft, output_file, ids, origin, axis, angle, errout)
    return False


def Rotate(craft, output_file, ids, origin, axis, angle, errout = sys.stderr):
    """
    Rotates multiple parts around one.
    """
    parts = craft.find("Parts")

    #For each part to be rotated.
    for part_id in ids:
        part = parts.get_filtered("id", str(part_id))
        #Calculate the new relative position
        rel_pos = Rot3d(Vector.from_css(part["position"]) - origin, axis, math.radians(angle))
        #Turn the rotation into Vectors, then rotate those vectors
        x, y, z = Rot_to_vect(Vector.from_css(part["rotation"]))
        z = Rot3d(z, axis, math.radians(angle))
        y = Rot3d(y, axis, math.radians(angle))
        x = Rot3d(x, axis, math.radians(angle))
        #Caluclate and save the parts absolute position
        part["position"] = (rel_pos + origin).css() #Add the offset of the axis back, and turn it back into a css
        #Calculate the new rotation, and save it
        part["rotation"] = Vect_to_rot(x,  y, z).css()

    #Save the final craft to the given output file
    craft.write(output_file)
    return True #True for Success
