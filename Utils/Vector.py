import math

class Vector(list):
    """
Creates a Vector class, on which simple operations can be performed item wise.
E.G. adding will add the respective items of the Vectors together.
"""
    @property
    def length(self):
        #returns a scalar which gives the length of the Vector.
        #In other words, it returns the value of the inner dot product.
        lst_sum = sum([item * item for item in self])
        return math.sqrt(lst_sum)
    
    def __add__(self, other):
        if isinstance(other, (Vector, list, tuple)):
            #adds the values in lst2 to those in lst1 (self)
            if len(self) != len(other):
                raise ValueError("Lists do not have the same dimensions")
            else:
                return Vector(a + b for a, b in zip(self, other))
        elif type(other) in (int, float):
            return Vector(i + other for i in self)
        else:
            raise TypeError("other has the wrong type")
    def __iadd__(self, other):
        return self + other
    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        if isinstance(other, (Vector, list, tuple)):
            #subtracts the values in lst 2 from lst 1 (self)
            if len(self) != len(other):
                raise ValueError("Vectors/Lists do not have the same dimensions")
            else:
                return Vector(a - b for a, b in zip(self, other))
        elif isinstance(other, (int, float)):
            return Vector(other - i for i in self)
    def __isub__(self, other):
        return self - other
    def __rsub__(self, other):
        return self - other
    
    def __mul__(self, other):
        #Multiplies each value in the vector with a given scalar, and returns the final list.
        if isinstance(other, (int, float)):
            return Vector(i * other for i in self)
        elif isinstance(other, (Vector, list, tuple)):
            #Multiplies each value in the vector with the corresponding value in the other list.append Especially useful for mirroring the scalar about an axis.
            if len(self) == len(other):
                return Vector(a * b for a, b in zip(self, other))
            else:
                raise ValueError("Vectors/Lists do not have the same dimensions")
        else:
            raise TypeError(f"Multiplier should be type int, float, Vector or List, not {type(other).__name__}.")
    def __imul__(self, other):
        #Multiplies each value in the vector with a given scalar, and returns the final list.
        if isinstance(other, (int, float)):
            return Vector(i * other for i in self)
        elif isinstance(other, (Vector, list, tuple)):
            #Multiplies each value in the vector with the corresponding value in the other list. Especially useful for mirroring the scalar about an axis.
            if len(self) == len(other):
                return Vector(a * b for a, b in zip(self, other))
            else:
                raise ValueError("Vectors/Lists do not have the same dimensions")
        else:
            raise TypeError(f"Multiplier should be type int, float, Vector or List, not {type(scalar).__name__}.")
    def __rmul__(self, other):
        return self * other

    def __abs__(self):
        return Vector(abs(i) for i in self)
    
    def __truediv__(self, other):
        #Divides each value in the vector with a given scalar, and returns the final list.
        if isinstance(other, (int, float)):
            return Vector(i / other for i in self)
        elif isinstance(other, (Vector, list, tuple)):
            #Divides each value in the vector with the corresponding value in the other list.
            if len(self) == len(other):
                return Vector(a / b for a, b in zip(self, other))
            else:
                raise ValueError("Vectors/Lists do not have the same dimensions")
        else:
            raise TypeError(f"Divider should be type int, float, Vector or List, not {type(other).__name__}.")
    def __rtruediv__(self, other):
        if isinstance(other, (Vector, list, tuple)):
            #Divides each value in the vector with the corresponding value in the other list.
            if len(self) == len(other):
                return Vector(a / b for a, b in zip(self, other))
            else:
                raise ValueError("Vectors/Lists do not have the same dimensions")
        else:
            raise TypeError(f"Cannot divide type {type(other).__name__} by type Vector.")

    def __round__(self, ndigits = None):
        return Vector(round(i, ndigits) for i in self)

    def __neg__(self):
        return Vector(-i for i in self)
    def __pos__(self):
        return Vector(i for i in self)
    def __abs__(self):
        return Vector(abs(i) for i in self)

    def __gt__(self, other):
        if isinstance(other, (int, float)):
            return all(i > other for i in self)
        elif isinstance(other, (Vector, list, tuple)):
            if len(self) == len(other):
                return all(a > b for a, b in zip(self, other))
            else:
                raise ValueError("Vectors/Lists do not have the same dimensions")
        else:
            raise TypeError(f"Cannot compare value of {type(other).__name__} to value of Vector.")


    
    def rotate(self, angle):
        """
        Rotates the vector clockwise for the given amount of degrees.
        Note: Only for 2d vectors.
        """
        if len(self) != 2:
            raise ValueError("Simple rotations are only available in two dimensional space.")
        else:
            angle = math.radians(angle)
            return Vector([self[0] * math.cos(angle) + self[1] * math.sin(angle),
                    - self[0] * math.sin(angle) + self[1] * math.cos(angle)])
    def rot90(self):
        """
        Rotates a 2d Vector 90 degrees clockwise. Faster than self.rotate(90).
        """
        if len(self) != 2:
            raise ValueError("Simple rotations are only available in two dimensional space.")
        return Vector([self[1], -self[0]])

    def rotate_3d(self, axis, angle):
        """
        Rotates self around axis for angle radians. A 90 degree rotation is in
        the same direction as self.cross(axis).
        """
        if not type(axis) in (Vector, list, tuple):
            raise TypeError(f"'axis' should be type Vector, list, or tuple, not type {type(axis).__name__}")
        elif len(self) != 3 or len(axis) != 3:
            raise ValueError("All vectors should have len 3")
        elif not type(angle) in (float, int):
            raise TypeError(f"'angle' should be type float, or int, not type {type(angle).__name__}")
        axis = Vector(axis).unit
        offset = self.projection(axis)
        v1 = self.orthogonal(axis)
        v2 = v1.cross(axis)
        return offset + math.cos(angle) * v1 + math.sin(angle) * v2

    def distance(self, lst_2):
        #Calculates the distance between two position vectors.
        return (self - lst_2).length

    def unit_vector(self):
        """
        Returns the unit vector of the original vector.
        """
        length = self.length
        unit = self / length
        return unit
    @property
    def unit(self):
        """
        Another way to acces a Vector's unit vector
        """
        return self.unit_vector()

    def shiftR(self):
        """
        Shifts all values such that the first value becomes the second, ..., the last becomes the first.
        """
        if len(self) == 0:
            return Vector([])
        else:
            return Vector([self[-1]] + [value for value in self[:-1]])

    def shiftL(self):
        """
        Shifts all values such that the first value becomes the last, second becomes first, ... .
        """
        if len(self) == 0:
            return Vector([])
        else:
            return Vector([value for value in self[1:]] + [self[0]])

    def dot(self, other):
        """
        Returns the dot product of two vectors of the same length
        """
        return sum(self * other)



    def cross(self, other):
        """
        Returns the (right handed) cross product for two vectors.
        """
        if len(self) != 3:
            raise ValueError("Cross product is not implemented for vectors with length other than 3")
        product = (self.shiftL() * other.shiftR()) - (self.shiftR() * other.shiftL())
        return product

    def projection(self, other):
        """
        Returns the projection of self onto other
        """
        proj = self.dot(other.unit) * other
        return proj

    def orthogonal(self, other):
        """
        Returns the component of self that is perpendicular to other
        """
        return self - self.projection(other)
    
    def __repr__(self):
        return "Vector(" + super().__repr__() + ")"

    def css(self, precision = None):
        """
        Returns the vector as a comma separated string
        """
        if precision is None:
            out_str = ",".join(f"{value}" for value in self)
        else:
            out_str = ",".join(f"{value:.{precision}f}" for value in self)
        return out_str
    @staticmethod
    def from_css(string, typ = float):
        """
        Extracts a vector from a comma separated string, and returns it.
        """
        string = string.removeprefix("[").removesuffix("]")
        string = string.removeprefix("(").removesuffix(")").strip(" ")
        return Vector(typ(i) for i in string.split(","))

    def Clamp(self, minimum, maximum):
        """
        Returns a value which is as close to value as possible, but is minimum <= value <= maximum.
        """
        if maximum < minimum:
            raise ValueError("Maximum must be >= Minimum")
        return Vector(max(minimum, min(value, maximum)) for value in self)
    
