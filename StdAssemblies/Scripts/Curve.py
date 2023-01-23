import sys
import math

from Utils.XML import XML
from Utils.Vector import Vector
from Utils.Vect3d import Rot_to_vect, Vect_to_rot
from Utils.Vect3d import Rotate as Rot3d

from .Verify import Verify

from Utils import SimpleUtils as SP
from Utils.DefaultParts import Fuselage, Sphere
from Utils.cfg import Unit


def Run(output_file, angle, radius, thickness, n, truncate, rounded, errout = sys.stderr):
    """
    Verifies all inputs, and runs the script if all inputs are valid.

    Add "Radius Type" option (inner radius, outer radius, mean radius, ...)
    """
    errors, output_file, n, angle, radius, thickness = \
            Verify(output_file, int_ = n, float_ = [angle, radius], range_ = thickness, errout = errout)
    if angle is not None and angle >= 180:
        print("Angle too large. May not be >= 180 degrees", file = errout)
        errors = True
    if n < 1 or (n == 1 and truncate):
        print("Too few segments to create curve", file = errout)
        errors = True
    if not errors:
        return Curve(output_file, angle, Unit(radius), thickness, n, truncate, rounded, errout = errout)
    return False

def Curve(output_file, angle, radius, thickness, n, truncate, rounded, errout = sys.stderr):
    """
    angle: The angle per segment.
    radius: The minimum distance to the origin of the centerline of the tube (e.g. for a square, 1/2 * the height).
    thickness: The thickness at the minimum radius point.
    n: The number of segments in the curve.
    truncate: Whether the edge fuselage pieces should be half-truncated.
    """
    #Corner correction flag: If True, the length of the fuselages will be
    # increased slightly to make sure the outer-most part of the fuselages
    # connects properly, at the expense of creating some artifacts at the
    # meeting point of the centerlines.
    corner_correction = not rounded
    sphere_corners = rounded
    #Start the assembly
    assembly = SP.SubAssembly("Curve")
    SP.init(assembly)
    #Calculate part properties / sizes
    #Note: Length has an additional *2 because it is in SP units, not [m]
    length = radius * 2*math.tan(math.radians(angle / 2))
    #Define the default rotation Vectors (initial rotation)
    x0 = Vector([0, 0, -1])
    y0 = Vector([0, 1, 0])
    z0 = Vector([1, 0, 0])
    p0 = [0, radius, 0]
    x_n = 0
    for i in range(n):
        part = Fuselage()
        #Set the part properties / size
        part["Fuselage.State"]["frontScale"] = f"{thickness(x_n)},{thickness(x_n)}"
        #Update the part rotation
        x = Rot3d(x0, [0, 0, 1], math.radians(i*angle))
        y = Rot3d(y0, [0, 0, 1], math.radians(i*angle))
        z = Rot3d(z0, [0, 0, 1], math.radians(i*angle))
        part["rotation"] = Vect_to_rot(x, y, z).css()
        #Part positions
        pos = Rot3d(p0, [0, 0, 1], math.radians(i*angle))
        facing = Rot3d([1, 0, 0], [0, 0, 1], math.radians(i*angle))
        # First node position
        if i == 0 and truncate:
            pos_0 = pos
        else:
            pos_0 = pos + length / 2 * facing
            if corner_correction:
                pos_0 += thickness(x_n) * math.tan(math.radians(angle/2)) / 4 * facing
        # Update the node position
        if truncate:
            x_n += 1/(n-1) * (0.5 if i == 0 or i == n-1 else 1)
        else:
            x_n += 1/n
        # Second node position
        if i == n-1 and truncate:
            pos_1 = pos
        else:
            pos_1 = pos - length / 2 * facing
            if corner_correction:
                pos_1 -= thickness(x_n) * math.tan(math.radians(angle/2)) / 4 * facing

        part["Fuselage.State"]["rearScale"] = f"{thickness(x_n)},{thickness(x_n)}"
        part["Fuselage.State"]["offset"] = f"0,0,{pos_0.distance(pos_1) * 2}"
        part["position"] = ((pos_0 + pos_1) / 2).css()
        SP.Add_part(part)
        if i: #If this is not the first part:
            #Connect the fuselage to the previous one
            SP.Connect(prev, part, 0, 1)
        prev = part
        if sphere_corners and i != n-1:
            sphere = Sphere()
            sphere["position"] = pos_1.css()#(Rot3d(p0, [0, 0, 1], math.radians(i*angle)) - \
#                                 Rot3d([length / 4, 0, 0], [0, 0, 1], math.radians(i*angle))).css()
            #Note: Size correction to account for discrepencies between spheres' "round" and
            # fuselages' "round". 4% increase showed the least noticeable gaps.
            sphere["ResizableShape.State"]["size"] = f"{1.04*thickness(x_n)}"
            SP.Add_part(sphere)
            SP.Connect(sphere, part, 0, 0)


    assembly.write(output_file)
    return True
