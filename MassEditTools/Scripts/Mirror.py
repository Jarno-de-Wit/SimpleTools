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
from .Flip import Flip_part
from Utils import SimpleUtils as SP

def Run(input_file, output_file, ids, origin, normal, errout = sys.stderr):
    """
    Verifies all inputs, and runs the script if all inputs are valid.
    """
    errors, craft, output_file, ids, origin, normal = \
            Verify(input_file, output_file, ids, origin, normal, errout = errout)

    if not errors: #If all data was input correctly:
        return Mirror(craft, output_file, ids, origin, normal, errout)
    return False


def Mirror(craft, output_file, ids, origin, normal, errout = sys.stderr):
    """
    Scales multiple parts relative to a given point.
    """
    parts = craft.find("Parts")
    normal = normal.unit

    SP.init(craft)
    for id_ in ids:
        part = parts.get_filtered("id", str(id_))
        new = SP.Copy(part)
        new = Flip_part(new)
        #Calculate the new part position
        pos = Vector.from_css(new["position"])
        pos -= 2 * (pos - origin).projection(normal)
        new["position"] = pos.css()
        #Turn the rotation into Vectors, then rotate those vectors
        x, y, z = Rot_to_vect(Vector.from_css(new["rotation"]))
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
        if "Wheel" in new["partType"]:
            new["rotation"] = Vect_to_rot(x, y, None).css()
        #Wings have a similar issue, except for having their symmetry axis in the
        # Y direction.
        elif "Wing" in new["partType"]:
            new["rotation"] = Vect_to_rot(x, None, z).css()
        else:
            new["rotation"] = Vect_to_rot(None, y, z).css()

    #Reconnect the new parts. Don't bother about connection points, since they
    # don't really matter anyway (at least, not here).
    SP.Reconnect(ids, 1)
    #Save the final craft to the given output file
    craft.write(output_file)
    return True
