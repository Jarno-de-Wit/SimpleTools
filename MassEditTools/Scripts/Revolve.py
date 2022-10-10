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
from Utils.Vect3d import Rotate as Rot3d

from .Verify import Verify
from Utils import SimpleUtils as SP

def Run(input_file, output_file, ids, origin, axis, ncopies, angle, errout = sys.stderr):
    """
    Verifies all inputs, and runs the script if all inputs are valid.
    """
    errors, craft, output_file, ids, origin, axis, ncopies, angle = \
            Verify(input_file, output_file, ids, origin, axis, int_ = ncopies, float_ = angle, errout = errout)

    if not errors: #If all data was input correctly:
        return Revolve(craft, output_file, ids, origin, axis, ncopies, angle, errout)
    return False


def Revolve(craft, output_file, ids, origin, axis, ncopies, angle, errout = sys.stderr):
    """
    Revolves multiple parts around one.
    """
    parts = craft.find("Parts")

    #Initialise  the Utils lib with the craft (to set max_id, etc.)
    SP.init(craft)
    for id_ in ids:
        part = parts.get_filtered("id", str(id_))
        for i in range(1, ncopies+1):
            new = SP.Copy(part)
            #Calculate the new relative position
            rel_pos = Rot3d(Vector.from_css(new["position"]) - origin, axis, math.radians(i*angle))
            #Turn the rotation into Vectors, then rotate those vectors
            x, y, z = Rot_to_vect(Vector.from_css(new["rotation"]))
            z = Rot3d(z, axis, math.radians(i*angle))
            y = Rot3d(y, axis, math.radians(i*angle))
            x = Rot3d(x, axis, math.radians(i*angle))
            #Caluclate and save the parts absolute position
            new["position"] = (rel_pos + origin).css() #Add the offset of the axis back, and turn it back into a css
            #Calculate the new rotation, and save it
            new["rotation"] = Vect_to_rot(x,  y, z).css()

    SP.Reconnect(ids, ncopies)
    #Save the final craft to the given output file
    craft.write(output_file)
    return True
