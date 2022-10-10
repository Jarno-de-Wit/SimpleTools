from .Vector import Vector

def is_int(value):
    return is_type(value, int)

def is_float(value):
    return is_type(value, float)

def is_vect(value):
    try:
        Vector.from_css(value)
        return True
    except ValueError:
        return False

def is_type(value, type_):
    try:
        type_(value)
        return True
    except ValueError:
        return False

def clamp(val, min_, max_, /):
    """
    Returns the value closest to val, that lies within the bounds of min_ and max_
    """
    return min(max(val, min_), max_)
