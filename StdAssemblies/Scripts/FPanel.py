import sys
import os
import math

from Utils.cfg import Unit
from Utils.DefaultParts import Fuselage
import Utils.SimpleUtils as SP
from functools import partial

from .Verify import Verify

def Run(output_file, coords, thickness, errout = sys.stderr):
    errors, output_file, *coords, thickness = Verify(output_file, pos2d = coords, float_ = thickness, errout = errout)

    if errors:
        return False

    FPanel(output_file, [Unit(c) for c in coords], Unit(thickness), errout)



def FPanel(output_file, coords, thickness, errout = sys.stderr):
    craft = SP.SubAssembly(os.path.splitext(os.path.basename(output_file))[0])
    SP.init(craft)
    #Rectify the coords, so turning to the right always goes towards the
    # inside of the panel
    midpoint = (coords[1] + coords[0]) / 2
    ray = (coords[1] - coords[0]).rot90().unit
    #Rotate the ray atan(pi/e) degrees, to hopefully prevent the ray from
    # exactly hitting the edge of a line segment, which could lead to
    # unpredictable results otherwise.
    ray = ray.rotate(49.13180624091392)
    #Count the number of intersected lines on the way out from the structure
    # If even, reverse the list so the line goes towards the inside of the body
    if not sum(intersect(midpoint, midpoint + 100 * ray, B0, B1) for B0, B1 in zip(coords[1:], coords[2:])) % 2:
        coords = list(reversed(coords))
        print("Reversed")

    success = bool(_FPanel(coords, thickness))
    craft.write(output_file)

def _FPanel(coords, thickness):
    if len(coords) <= 2:
        return None
    elif len(coords) == 3: #Simple optimisation. Could also run the normal procedure, but that would be slower
        return triangle(coords, thickness)
    else:
        midpoint = (coords[0] + coords[1]) / 2
        normal = (coords[1] - coords[0]).unit.rot90()
        key_func = partial(sort_func, normal, midpoint)
        for i, point in sorted(enumerate(coords[2:]), key = key_func):
            #If the line from any of the corners to the point intersects a line,
            # and thus the triangle would cut through empty space: skip it
            if intersections(coords[2:], coords[0], point, exclude = i) or \
               intersections(coords[2:], coords[1], point, exclude = i):
                continue
            #Increase i by 2 again to account for cutting the first 2 items
            # inside enumerate
            i += 2
            print(f"Chosen point: {i} coords[i]")
            #Create the new fuselage segment
            fus = triangle(coords[:2] + coords[i:i+1], thickness)

            #Create the rest of the fuselage segments, and connect them to fus (if it exists)
            if (left := _FPanel(coords[:1] + coords[i:], thickness)) and fus:
                SP.Connect(fus, left, 0, 0)
            if (right := _FPanel(coords[i:i+1] + coords[1 : i], thickness)) and fus:
                SP.Connect(fus, right, 0, 0)
            #If fus existed: return it. Else, do some magic to connect the other fuselages, and return one of those two.
            if fus:
                return fus

            #Connect both flanking fuselages to maintain integrity (if both exist)
            if right and left:
                SP.Connect(right, left, 0, 0)

            #Return any of the two fuselages. Or is used or the case only one of the
            # two fuselages was valid / created, in which case that fuselage should
            # be passed on to be connected to the main structure.
            return right or left

def sort_func(normal, midpoint, point):
    """
    The sorting function used for ranking other points as optimal locations to triangle to
    """
    #Remove the "debris" present from enumerate()
    point = point[1]
    #Calculate the sorting value
    lateral_offset = abs((point - midpoint).dot(normal.rot90()))
    forward_offset = (point - midpoint).dot(normal)
    return lateral_offset / forward_offset if forward_offset != 0 else math.inf

def triangle(coords, thickness):
    """
    Creates a triangular fuselage which connects the given coordinates
    Coordinates should be in clockwise direction.
    """
    #If the coordinates are practically on one line, don't make a fuselage.
    # The result would not look good.
    # Cutoff angle is approx 2.56 degrees
    if (coords[1] - coords[0]).unit.dot((coords[2] - coords[0]).unit) >= 0.999:
        return None
    #Pass in three coords to return a triangle fuselage that fits between those
    fus = Fuselage()
    SP.Add_part(fus)
    print("id: "+ fus["id"])
    fus["Fuselage.State"]["cornerTypes"] = "0,0,0,0,0,0,0,0"
    #Set front and rear scale.
    #Note: Thickness multiplied with 2 to transform from [meter] back to [fuselage unit]
    fus["Fuselage.State"]["frontScale"] = f"0,{2*thickness}"
    fus["Fuselage.State"]["rearScale"] = f"{2*(coords[1]-coords[0]).length},{2*thickness}"
    #Determine the edges
    edges = [coords[(i+1)%3] - coords[i] for i in range(3)]
    #Find the midpoint between the first two points
    mid = (coords[0] + coords[1]) / 2
    normal = (coords[1] - coords[0]).rot90().unit
    length = (coords[2] - mid).dot(normal)
    if length < 0:
        raise RuntimeError(f"Required length < 1. This should not happen. DEBUG:{coords}")
    offset = (coords[2] - mid).dot((coords[1] - coords[0]).unit)
    fus["Fuselage.State"]["offset"] = f"{2*offset},0,{2*length}"
    #The position is the location between the midpoint of 1,2 and 
    pos = (mid + coords[2]) / 2
    fus["position"] = f"{pos[0]},0,{pos[1]}"
    fus["rotation"] = f"0,{math.degrees(math.atan2(edges[0][1], -edges[0][0]))},0"
    return fus


def intersect(A0, A1, B0, B1):
    """
    Returns True if the lines delimited by the coordinates intersect
    """
    normal_A = (A1 - A0).rot90()
    normal_B = (B1 - B0).rot90()
    if (A0 - B0).dot(normal_B) * (A1 - B0).dot(normal_B) <= 0 and \
       (B0 - A0).dot(normal_A) * (B1 - A0).dot(normal_A) <= 0:
        return True
    else:
        return False

def intersections(coords, origin, end, exclude = None):
    intersects = 0
    for i, (coord_0, coord_1) in enumerate(zip(coords, coords[1:])):
        #If any of the two coordinates is the excluded one, skip
        if exclude is not None and (i == exclude or i + 1 == exclude):
            continue
        if intersect(coord_0, coord_1, origin, end):
            intersects += 1
    return intersects
