from Vector import Vector
from Vect_3d import Rotate, Step_rotator
import SimpleUtils as SU

import sys
import math
import copy

sin = lambda x: math.sin(math.radians(x))
cos = lambda x: math.cos(math.radians(x))
tan = lambda x: math.tan(math.radians(x))


def Build(n_segments, angle, radius, thickness, corners, align = True, center = False):
    """
    n_segments: Number of segments the circle is to be made of.
    angle: The total angle the circle should cover
    radius: The radius to the midpoint of each section (except corners if align == True)
    thickness: The thickness of the circle
    corners: The corners of the fuselages used
    align: Determines whether the outer two sections of the circle should be aligned with the in-/outgoing lines. If true, the outer two fuselages will only have half length

    NOTE: Rotation point of front section lies on the same height / offset from the bottom, as the centerline of the root section.

    => L_eff = L*cos(alpha/2) + Rise*sin(alpha/2) - L_eff*sin(alpha/2)
    """
    # The angle per segment, is the total angle, minus the number of corners.
    # If align = True, there is 1 less effective corner, as the last segments are really only half segments.
    angle_step = angle / (n_segments - align)
    if angle_step > 30:
        print("Warning: too little segments for adpted curve", file = sys.stdout)
    print(f"{angle_step = }")

    length = 2 * radius * tan(angle_step)

    r_vect = Vector([0, 1, 0]) * radius

    subassembly = SU.Subassembly("Curve")
    parts = subassembly.find("Parts")
    size = f"{thickness},{thickness / cos(angle_step/2)}"

    # If align == True: Rotate the vector slightly to account for the first
    #   fuselage being only half, thus needing to be taken into account differently.
    if align:
        r_vect2 = r_vect.rotate_3d([0, 0, 1], math.radians(angle_step))
        rotator = Step_rotator(r_vect2, [0, 0, 1], math.radians(angle_step), n_segments - 2)
        angles = iter([angle_step * (i + 1) for i in range(n_segments - 2)])
        part_0 = SU.Fuselage()
        part_0["position"] = ( r_vect / cos(angle_step / 4) ).css(6)
        part_0["rotation"] = "0,90,0"
        part_0["Fuselage.State"]["cornerTypes"] = corners
        part_0["Fuselage.State"]["offset"] = f"0,0,{length/2:.7f}"
        part_0["Fuselage.State"]["inletSlant"] = f"{angle_step / 120:.7f}"
        parts.append(part_0)
    else:
        rotator = Step_rotator(r_vect, [0, 0, 1], math.radians(angle_step), n_segments)
        angles = iter([angle_step * i for i in range(n_segments)])

    for r in rotator:
        fuselage = SU.Fuselage()
        fuselage["Fuselage.State"]["cornerTypes"] = corners
        fuselage["Fuselage.State"]["frontScale"] = size#f"{thickness},{thickness/cos(angle_step/2)}"
        fuselage["Fuselage.State"]["rearScale"] = size
        fuselage["position"] = r.css(7)
        fuselage["rotation"] = f"{(next(angles)+180-angle_step/2) % 360 - 180},90,0"
        fuselage["Fuselage.State"]["offset"] = f"0,{sin(angle_step/2)*length},{cos(angle_step/2)*length + sin(angle_step/2)*length*tan(angle_step)/2}"
        fuselage["Fuselage.State"]["inletSlant"] = f"{angle_step / 60 / cos(angle_step)}"
        parts.append(fuselage)

    if align:
        part_n = SU.Fuselage()
        part_n["position"] = ( r_vect.rotate_3d([0, 0, 1], math.radians(angle)) / cos(angle_step / 4) ).css(7)
        part_n["rotation"] = f"{(angle+180 - angle_step/2) % 360 - 180},90,0"
        part_n["Fuselage.State"]["cornerTypes"] = corners
        part_n["Fuselage.State"]["offset"] = f"0,{sin(angle_step/2)*length/2},{cos(angle_step/2)*length/2}"
        part_n["Fuselage.State"]["inletSlant"] = f"{angle_step / 120 / cos(angle_step/2)}"
        parts.append(part_n)
   
    for i in range(n_segments - 1):
        SU.Connect(subassembly, parts[i]["id"], parts[i+1]["id"], 1, 0)
    subassembly.write("Circ.xml")
    return

Build(12, 360, 2, 1, "1,2,1,0,1,2,1,0", False)
