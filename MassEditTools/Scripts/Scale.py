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

from .Verify import Verify

def Run(input_file, output_file, ids, origin, scale, mode, errout = sys.stderr):
    """
    Verifies all inputs, and runs the script if all inputs are valid.
    """
    errors, craft, output_file, ids, origin, scale = \
            Verify(input_file, output_file, ids, origin, float_ = scale, errout = errout)

    mode = {"Size + Position": 1,
            "Part Size": 2,
            "Position": 3}.get(mode, 0)
    if mode == 0:
        print("Invalid scaling mode", file = errout)
        errors = True

    if not errors: #If all data was input correctly:
        return Scale(craft, output_file, ids, origin, scale, mode, errout)
    return False


def Scale(craft, output_file, ids, origin, scale, mode, errout = sys.stderr):
    """
    Scales multiple parts relative to a given point.
    """
    parts = craft.find("Parts")

    for id_ in ids:
        part = parts.get_filtered("id", str(id_))
        if mode in [1, 2]:
            part_scale = Vector.from_css(part.attributes.get("scale", "1,1,1"))
            part["scale"] = (part_scale * scale).css()
        if mode in [1, 3]:
            pos = Vector.from_css(part["position"])
            part["position"] = (pos * scale).css()

    #Save the final craft to the given output file
    craft.write(output_file)
    return True
