"""
An extension to the Vector class / library, containing special vector operations
for 3d use cases.
"""

import math
from .Vector import Vector


def Rot_to_vect(rotation):
    """
    Takes a rotation in Euler angle form in degrees, and turns it into a vector
        representation.
    Returns(x', y', z')
    In this, x', y', and z' represent the direction of the local x, y, and z in
        in the absolute reference frame. Logically, this leads to the conclusion
        that if no rotation has taken place, x' == x, y' == y, and z' == z.
    The order in which the rotations are executed is:
        1. Rotate the amount of degrees given around the x-axis.
        2. Rotate the amount of degrees given around the new y'-axis.
        3. Rotate the amount of degrees given around the especially new z'-axis.
    While rotating around '(prime) axis does lead to the existence of
        singularities, it is still convenient in many situations.
    Note: The axis system used for these transformations does not matter, so
        long as the rotation angles are given in the same axis system.
    """
    #Extract all rotations from the list, so they are easier to access.
    rot_x = math.radians(rotation[0])
    rot_y = math.radians(rotation[1])
    rot_z = math.radians(rotation[2])
    #Construct the forward facing vector. This is thus the main direction.
    facing_x = math.cos(rot_x) * math.sin(rot_y)
    facing_y = - math.sin(rot_x)
    facing_z = math.cos(rot_x) * math.cos(rot_y)
    facing = Vector([facing_x, facing_y, facing_z])
    """
    rot_y - math.atan2(math.sin(rot_z) * math.sin(rot_x), math.cos(rot_z))
    ^^^^^^ The part above give the angle of the line from the positive X-axis in the x-z plane, clockwise when looking from negative y to positive y (aka downwards).
    This is used in the calculations of right_x and right_z.
    """
    #Calculate the total horizontal component of the right facing vector.
    horizontal_right_length = math.sqrt(1 - (math.cos(rot_x) * math.sin(rot_z))**2)
    #Construct the right facing vector.
    right_x = horizontal_right_length * math.cos(rot_y - math.atan2(math.sin(rot_z) * math.sin(rot_x), math.cos(rot_z)))
    right_y = math.cos(rot_x) * math.sin(rot_z)
    right_z = horizontal_right_length * -math.sin(rot_y - math.atan2(math.sin(rot_z) * math.sin(rot_x), math.cos(rot_z)))
    right = Vector([right_x, right_y, right_z])
    """
    rot_y - math.atan2(math.sin(rot_z), math.cos(rot_z) * math.sin(rot_x))
    ^^^^^^ The part above gives the angle of the line from the positive z-axis in the x-z plane, clockwise when looking from negative y to positive y (aka downwards).
    This is used in the calculations of down_x and down_z.
    """
    #Calculate the horizontal component of the down facing vector.
    horizontal_down_length = math.sqrt(1 - (math.cos(rot_x) * math.cos(rot_z))**2)
    """
    Other ways to write the horizontal length:
    horizontal_down_length = math.sqrt((math.sin(rot_z))**2 - (math.cos(rot_x) * math.sin(rot_x))**2)
    horizontal_down_length = math.sqrt((math.sin(rot_z))**2 - (math.sin(rot_z) * math.sin(rot_x))**2 + (math.sin(rot_x))**2)
    """
    #Construct the vector pointing down for the object. (For redundancy)
    down_x = horizontal_down_length * math.sin(rot_y - math.atan2(math.sin(rot_z), math.cos(rot_z) * math.sin(rot_x)))
    down_y = math.cos(rot_x) * math.cos(rot_z)
    down_z = horizontal_down_length * math.cos(rot_y - math.atan2(math.sin(rot_z), math.cos(rot_z) * math.sin(rot_x)))
    down = Vector([down_x, down_y, down_z])
    #right = facing.cross(down)
    #In the end, right should be the cross product of (facing x down).
    return (right, down, facing) #x', y', z'

def Vect_to_rot(right = None, down = None, facing = None):
    """
    Takes at least two vectors in a right handed axis system, and turns it into
        a set of Euler angles. If three vectors are given, all three are used.
        If two are given, the third one is automatically constructed from the
        given vectors.
    The output will always have the rotation around the x-axis be -90 <= x <= 90
    """
    if (not facing ) + (not right ) + (not down ) > 1: #If at least two vectors are undefined:
        raise RuntimeError("At least two vectors are required to get a rotation.")
    #Construct any missing vector from the other two vectors (using the cross product).
    elif not(facing):
        down = Vector(down)
        right = Vector(right)
        facing = right.cross(down)
    elif not(right):
        facing = Vector(facing)
        down = Vector(down)
        right = down.cross(facing)
    elif not(down):
        right = Vector(right)
        facing = Vector(facing)
        down = facing.cross(right)
    #Find the x-rotation (pitch)
    rot_x = math.asin(-facing[1]) #The pitch angle is determined solely based on the verticality of the heading vector. This is possible since any pitch outside of the -90 to 90 degree range, can also be accomplished using other rotations.
    #print(f"rot_x = {math.degrees(rot_x)}")
    #Find the z-rotation (roll, around forward facing axis)
    rot_z = math.atan2(right[1], down[1])
    #print(f"rot_z = {math.degrees(rot_z)}")
    """
    Select which vectors give the most accurate representation about the
    rotations around the y-axis (downwards facing axis). This vector will be used
    to determine the angles. This reduces the likelyhood of floating point
    errors/singularities creeping in and invalidating the result.
    """
    if (right * [1, 0, 1]).length > (down * [1, 0, 1]).length: #If the "right" arm is more horizontal than the "down" arm:
        #Use the "right" vector for finding the required angle, since this won't face any singularities.
        #The yaw the right vector is currently at: (atan2(-z, x))
        target_yaw = math.atan2(-right[2], right[0])
        #print(f"Angle from x: {math.degrees(target_yaw)}")
        #The yaw component caused by rolling:
        roll_yaw = math.atan2(math.sin(rot_z) * math.sin(rot_x), math.cos(rot_z))
        #print(f"Roll yaw from x: {math.degrees(roll_yaw)}")
        #rot_y is the difference between the target, and what can "be explained" by the yaw caused by rolling.
        rot_y = target_yaw + roll_yaw
    else: #If the "down" arm is more horizontal than the "right" arm:
        #Use the down vector for finding the required angle, since this will probably be more accurate.
        #The yaw the down vector is currently at: (atan2(x, z))
        target_yaw = math.atan2(down[0], down[2])
        #print(f"Angle from z {math.degrees(target_yaw)}")
        #The yaw component caused by rolling:
        roll_yaw = math.atan2(math.sin(rot_z), math.cos(rot_z) * math.sin(rot_x))
        #print(f"Roll yaw from z: {math.degrees(roll_yaw)}")
        #rot_y is the difference between the target, and what can "be explained" by the yaw caused by rolling.
        rot_y = target_yaw + roll_yaw

    #Turn all values into degrees, and, where necessary, limit the values to -180 to 180.
    rot_x = math.degrees(rot_x)
    rot_y = ((math.degrees(rot_y) + 180) % 360) - 180
    rot_z = math.degrees(rot_z)
    rotation = Vector([rot_x, rot_y, rot_z])
    return rotation

def Rotate(vect, axis, angle):
    """
    Creates a vector, that has the same length as the original vector, but is
        rotated around the axis by a certain angle.
    """
    #Turn both the vector to be rotated, and the axis, into an actual Vector.
    vect = Vector(vect)
    axis = Vector(axis).unit
    #Determine the parallel component of the vector to the axis.
    offset = vect.projection(axis)
    #Create two vectors, at a 90 degree angle from each other and the axis, with v1.projection(vect) == v1.
    v1 = vect.orthogonal(axis)
    v2 = axis.cross(v1)
    return offset + math.cos(angle) * v1 + math.sin(angle) * v2

def Rotator(vect, axis, angle, steps, include_0 = True, include_final = False):
    """
    Creates an iterable that rotates a vector around an axis in n steps.
    """
    #Turn both the vector to be rotated, and the axis, into an actual Vector.
    vect = Vector(vect)
    axis = Vector(axis).unit
    #Determine the parallel component of the vector to the axis.
    offset = vect.projection(axis)
    #Create two vectors, at a 90 degree angle from each other and the axis, with v1.projection(vect) == v1.
    v1 = vect.orthogonal(axis)
    v2 = axis.cross(v1)
    if not include_0:
        steps += 1
        #Raise steps by 1, to account for 0 being excluded in the range.
    step_limit = steps
    if include_final:
        steps -= 1
        #Reduce steps by 1, so the division will lead to 'angle' degrees also being included.
        #Else, the last item would be rotated one part less, as max(range(i)) == i - 1
    #Rotate the vectors by combining v1 and v2 in the right proportions.
    for step in range(not(include_0), step_limit):
        angle = math.radians(angle / steps * step)
        yield (offset + math.cos(angle) * v1 + math.sin(angle) * v2)

def Step_rotator(vect, axis, angle, steps):
    """
    Creates an iterable that rotates a vector around an axis in n steps, with
        each step increasing the rotation by 'angle' degrees.
    """
    vect = Vector(vect)
    for step in range(steps):
        yield vect.rotate_3d(axis, step * angle)
