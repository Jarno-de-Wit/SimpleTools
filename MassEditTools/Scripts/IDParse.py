"""
Contains the parser that is used to parse the expressions for selecting certain parts from a craft.

Data types:
ID lists: set
Attribute: str
Attribute Index: [str, int]
Value: float, int, Vector
"""
import sys
try:
    from .ParseLib import *
    from Utils.XML import XML
    from Utils.Vector import Vector
except ImportError: #For debugging purposes. Allows this to be run as standalone locally
    from ParseLib import *
    from XML.XML import XML
    from Vector import Vector

#===============================<     setup     >===============================

DEBUG = print
#Uncomment below to send DEBUG to void()
DEBUG = lambda *args, **kwargs: None

all_parts = set()
__errout = sys.stderr
parts = XML()

class ParseError(Exception):
    pass

def Warn(msg):
    """
    Prints the warning message to errout, but does not obstruct program flow
    """
    global __errout
    print(msg, file = __errout)

#===============================< op definitions >==============================

def AND(left, right):
    left = PartList(left)
    right = PartList(right)
    return left.intersection(right)

def OR(left, right):
    left = PartList(left)
    right = PartList(right)
    return left.union(right)

def XOR(left, right):
    left = PartList(left)
    right = PartList(right)
    return left.__xor__(right)

def NOT(left, right):
    if left.strip(" \t"):
        Warn("Warning: Left side of 'NOT' is not empty")
    right = PartList(right)
    return all_parts.__xor__(right)

def range_(left, right):
    left = PartList(left)
    right = PartList(right)
    if len(left) != 1 or len(right) != 1:
        raise ParseError("Invalid range expression")
    min_, max_ = sorted([int(left.pop()["id"]), int(right.pop()["id"])])
    return set(part for part, val in Select("id") if min_ <= int(val) <= max_)

def brackets(left, right):
    if left.strip(" \t"):
        Warn("Warning: Left side of brackets is not empty")
    #counts = smart_count(right, ["(", ")"])
    inside, _, index = smart_split(right, ")", 1)
    parts = PartList(inside)
    if not index.strip(" \t"):
        return parts
    else:
        #Do indexing on the ids
        part_val = Index(parts, index)
        if part_val is None:
            raise ParseError(f"Part selection criteria too strict")
        return part_val #Return the part or value from the given index

def comp(path, value, test):
    tgt_value = Value(value, path)
    if isinstance(tgt_value, XML):
        raise ParseError("Can not compare XML objects directly")
    try:
        #Return each value for which 1. tgt is a wildcard, or 2. the test is successful
        return set(part for part, val in Select(path) if  tgt_value is None or test(val, tgt_value))
    except TypeError:
        raise ParseError("Cannot compare Part-Values with given operator (incorrect type?)")

def eq(path, value):
    return comp(path, value, lambda a, b: a == b)
def eq_ci(path, value): #Case insensitive
    return comp(path, value, lambda a, b: str(a).lower() == str(b).lower())

def neq(path, value):
    #Special case, because != to wildcard should return all parts that don't have the attribute
    # equivalent to "!(path = *)"
    tgt_value = Value(value, path)
    if isinstance(tgt_value, XML):
        raise ParseError("Can not compare XML objects directly")
    if tgt_value is None: #If the tgt is a wildcard
        return all_parts.__xor__(set(part for part, val in Select(path)))
    return set(part for part, val in Select(path) if val != tgt_value)
def neq_ci(path, value):
    #Special case, because != to wildcard should return all parts that don't have the attribute
    # equivalent to "!(path = *)"
    tgt_value = Value(value, path)
    if isinstance(tgt_value, XML):
        raise ParseError("Can not compare XML objects directly")
    if tgt_value is None: #If the tgt is a wildcard
        return all_parts.__xor__(set(part for part, val in Select(path)))
    return set(part for part, val in Select(path) if str(val).lower() != str(tgt_value).lower())

def gt(path, value):
    return comp(path, value, lambda a, b: a > b)

def lt(path, value):
    return comp(path, value, lambda a, b: a < b)

def geq(path, value):
    return comp(path, value, lambda a, b: a >= b)

def leq(path, value):
    return comp(path, value, lambda a, b: a <= b)

def contains(path, value):
    return comp(path, value, lambda a, b: str(b) in str(a))
def contains_ci(path, value):
    return comp(path, value, lambda a, b: str(b).lower() in str(a).lower())

def in_(path, value):
    return comp(path, value, lambda a, b: str(a) in str(b))
def in_ci(path, value):
    return comp(path, value, lambda a, b: str(a).lower() in str(b).lower())

def includes(path, value): #If the string contains the word as a "separate" word
    return comp(path, value, lambda a, b: str(b) in str(a).split())
def includes_ci(path, value): #If the string contains the word as a "separate" word
    return comp(path, value, lambda a, b: str(b).lower() in str(a).lower().split())

#===============================<   Subspaces   >===============================

class Volume():
    def __gt__(self, other):
        return self.calc(other) > self.limit
    def __geq__(self, other):
        return self.calc(other) >= self.limit
    def __lt__(self, other):
        return self.calc(other) < self.limit
    def __leq__(self, other):
        return self.calc(other) <= self.limit
    def __eq__(self, other):
        return self.calc(other) == self.limit
    def __neq__(self, other):
        return self.calc(other) != self.limit

class Radius(Volume):
    def __init__(self, left, right):
        if left.strip(" \t"):
            Warn("Left side of Radius is not empty")
        pos, _, limit = smart_split(right.strip(" \t").removesuffix(")"), ";")
        if _ is None:
            raise ParseError("Radius does not contain two values. Did you use the right separator (;)?")
        self.pos = Value(pos, "position")
        if not isinstance(self.pos, Vector):
            raise ParseError("Radius root location is invalid type (expected Vector, is type '{type(self.pos).__name__}')")
        self.limit = Value(limit)
        if not isinstance(self.limit, (int, float)):
            raise ParseError("Radius is invalid type (expected float or int, is type '{type(self.limit).__name__}')")

    def calc(self, other):
        if isinstance(other, XML):
            try:
                other = Vector.from_css(other["position"])
            except IndexError:
                raise ParseError("Left side of compare does not yield Part XML tags (missing 'position' attribute).")
        elif not isinstance(other, Vector):
            raise ParseError("Selector does not return right value type (expected Part XML or Vector, is '{type(other).__name__}'")
        return (other - self.pos).length

class Plane(Volume):
    pass

#===============================<    op list    >===============================

operators = [
    ({",": OR}, 0),
    ({"&": AND, "AND": AND, "|": OR, "OR": OR, "^": XOR, "XOR": XOR}, 0),
    ({"!": NOT}, 0),
    ({"=": eq, "==": eq, "!=": neq, ">": gt, "<": lt, ">=": geq, "<=": leq,
      "contains": contains, "*=": contains, "in": in_, "|=": in_, "~=": includes,
      # Case insensitive versions:
      "?=": eq_ci, "?==": eq_ci, "?!=": neq_ci, "?*=": contains_ci, "?|=": in_ci,
      "?~=": includes_ci}, 0),
    ({"~": range_}, 0),
    ({"Radius": Radius, "Plane": Plane}, 0),
    ({"(": brackets}, 0),
             ]

shortcuts = {"pos": "position",
             "x": "position[0]",
             "y": "position[1]",
             "z": "position[2]",
             }

#===============================<  parse logic  >===============================

def init(craft = None, errout = None):
    """
    craft: The craft (as XML) which should be used.
    errout: The error output.
    """
    global all_parts, __errout, parts, errors
    #Setup:
    __errout = errout
    if isinstance(craft, XML):
        parts = craft.find("Parts")
        all_parts = set(parts.database)
    elif craft is None:
        parts = XML()
        all_parts = set()
        __errout = None #Disable errout when no craft is given to prevent the output being spammed with e.g. "too few parts"
    else:
        raise TypeError("Incorrect craft type")

def parse(expr, catch_errors = True, /):
    """
    Parses the part selection expression, and turns it into a list of part IDs
    expr: The expression to be parsed
    errors: Whether errors should be printed. False to disable output for this time.
    """
    global __errout
    #Try to parse
    try:
        if not expr.strip(" \t"):
            raise ParseError("No part selection expr entered")
        return IDList(expr)
    except ParseError as e: #If an error occured, and error printing is enabled, print the error.
        if not catch_errors:
            raise
        elif e.args:
            print(e.args[0], file = __errout)

def parse_val(expr, path = None, errors = True):
    """
    Parses the value selection expression, and turns it into a list of part IDs
    expr: The expression to be parsed
    errors: Whether errors should be printed. False to disable output for this time.
    """
    #Try to parse
    try:
        if not expr.strip(" \t"):
            raise ParseError("No Value expr entered")
        return Value(expr, path)
    except ParseError as e: #If an error occured, and error printing is enabled, print the error.
        if e.args and errors != False:
            print(e.args[0], file = errout)

def Part(id_):
    if isinstance(id_, (list, tuple, set)):
        return set(sum((parts.get_filtered_all("id", str(val)) for val in id_), start = []))
    return parts.get_filtered("id", str(id_))

def IDList(expr):
    """
    Returns list of all part IDs of the parts that should be included based on the relevant section of the expression.
    """
    return sorted(set(int(part["id"]) for part in PartList(expr.strip(" \t"))))


def PartList(expr):
    """
    Returns a list of all parts that should be included based on the relevant section of the expression.

    Technically doesn't have to return a part list, in case "brackets" are called with an index, but I don't feel like renaming this function for that exception, not do I feel like having two copies of this code for that purpose only.
    """
    if isinstance(expr, set):
        if all(isinstance(part, XML) for part in expr):
            return expr
        else:
            return set(parts.get_filtered("id", str(i)) for i in expr)
    expr = expr.strip(" \t")
    if not expr: #An empty expression is interpreted as a set of no parts (to allow "1,2,3," to still be a valid input)
        return set()
    elif expr.isdigit():
        return set(parts.get_filtered_all("id", expr)) #Automatically returns an empty set if it doesn't exist
    elif expr.lower() == "root":
        try:
            return {[part for part, val in Select("Cockpit.State/primaryCockpit") if Value(val, is_expr = False) == True][0]}
        except IndexError:
            raise ParseError("Could not find craft root part")
    elif expr.lower() == "all":
        return set(parts.database)

    #Now, on to the actual parsing
    DEBUG(f"Got expression: {expr}")
    for op_dict, search_dir in operators:
        #Find the first operator that isn't inside brackets. If None are there, move on to the next operator
        left, operator, right = smart_split(expr, list(op_dict), search_dir)

        if operator:
            DEBUG(f"Parsed with operator '{operator}' and left '{left}' and right '{right}'")
            return op_dict[operator](left, right)


    raise ParseError("Invalid part selection expression")


def listIDs(craft = None):
    if craft:
        return [int(part["id"]) for part in craft.find_all("Part")]
    else:
        return []

def Select(attrs, parts = None):
    """
    Returns a list of parts, and their respective values for the given path

    Works pretty well, and shouldn't cause any crashes, but does have some of limitations on replacements
    """
    global tmp, errors, all_parts
    none = XML("None") #Define a unconnected "none" XML object, which is used as an empty pointer to prevent crashes
    warn_shown = False
    attrs = attrs.split("/")
    values = []
    out = []
    if parts is None:
        parts = globals()["parts"].database
    elif isinstance(parts, XML):
        parts = [parts]
    for part in parts:
        tmp = [part] #Save part to tmp variable to allow for marching
        for attr in attrs:
            attr = shortcuts.get(attr, attr) #Can be improved still
            if "[" in attr:
                attr, indices = attr.removesuffix("]").split("[")
                indices = indices.replace("*", ":").replace(" ", "").replace("\t", "") #Replace * with : to more easily create a slice
                tmp = [Slice(i.find_all(attr) or i.find_all(f"{attr}.State") or i.attributes.get(attr, none), indices, True) for i in tmp]
                #Join all nested lists together again
                tmp = sum(tmp, [])

            else:
                tmp = [i.find(attr) or i.find(f"{attr}.State") or i.attributes.get(attr, none) for i in tmp]

        try: #Try to convert all values to the desired part type
            values.extend([(part, Value(value, is_expr = False)) for value in tmp if value is not none]) #Add the values to the list of id-value combinations
        except TypeError:
            raise
            if not warn_shown:
                Warn(f"Incomplete path '{('/').join(attrs)}' (returns XML object, not value)")
                warn_shown = True

    return list(filter(lambda x: x[1] is not None, values)) #Filter all "invalid" values

def Value(inp, path = None, is_expr = True):
    """
    Converts a given input into a value

    inp: The string that is to be converted to a value
    path: Optional - The default path that should be followed if the expression is a part selection expression, which returns a part, and not yet a value.
    is_expr: Whether the value is allowed to be interpreted as an expression. Present to prevent XML values to be interpreted as expressions

    Is used for converting XML attributes into values
    Is used for converting user-input value expressions into values
    """
    global errors
    if isinstance(inp, (int, float)): #If the value is already a number, it must have been pre-parsed somehow. Anyway, just return it.
        return inp
    elif isinstance(inp, str):
        string = inp.strip(" \t")
        if string[:1] in ['"', "'"]:
            return string[1:-1]
        elif string == "*": #Wildcard
            return None
        elif string.lower() == "true":
            return True
        elif string.lower() == "false":
            return False
        else:
            try: return int(string)
            except ValueError: pass

            try: return float(string)
            except ValueError: pass

            if inp[:1] != "(": #Prevent (x) from being interpreted as a 1-length vector :)
                try: return Vector.from_css(string)
                except ValueError: pass
        if not is_expr: #If the value is any of the basic data types, it must be a string
            return inp
        #Alternatively, run through the parse loop
        #If the given input is not a value, and a potential path is given:
        try:
            parts = PartList(inp)
        except ParseError: #If the result was not a valid expression, return the input, as it must have been a string
            return inp
        if isinstance(parts, Volume):
            return parts
        elif isinstance(next(iter(parts), None), XML) and path is not None:
            ids, parts = zip(*Select(path, parts)) #Select the values, and extract them to parts
        if len(parts) == 0:
            #Just to exit without causing a crash
            raise ParseError("Part-Value selection parameters too strict")
        elif len(parts) >= 2:
            raise ParseError("Part-Value selection parameters not strict enough")
        return parts[0]
    elif isinstance(inp, XML):
        return inp


    return None #If it was no real value

def Slice(lst, idx, force_lst = False):
    """
    Creates a sliced list based on the indices given
    """
    idx = idx.removeprefix("[").removesuffix("]")
    if isinstance(lst, str):
        lst = Vector.from_css(lst)
    elif isinstance(lst, set):
        lst = tuple(lst)
    # If only a single item is to be returned, don't create a slice (because that will go wrong)
    if idx.removeprefix("-").isdecimal():
        if -len(lst) - 1 < int(idx) < len(lst):
            if force_lst:
                return [lst[int(idx)]]
            else:
                return lst[int(idx)]
        else:
            raise ParseError("Invalid index (index out of range)")
    slice_ = slice(*(int(i) if i.removeprefix("-").isdecimal() else None for i in idx.split(":")))
    start, stop, step = slice_.indices(len(lst))
    return [lst[i] for i in range(start, min(stop + 1, len(lst)), step)]

def Index(parts, indices):
    if isinstance(parts, XML):
        parts = [parts]
    for idx in indices.split("]"):
        idx = idx.removeprefix("[")
        if not idx: #If this is the last item, continue
            continue
        if all(i.removeprefix("-").isdecimal() for i in idx.split(":")):
            parts = Slice(parts, idx, True)
        else:
            _, parts = zip(*Select(idx, parts)) #Technically returns values, not parts
    return parts

if __name__ == "__main__":
    craft = XML.XMLFile("Wisp.xml")
    print(parse("y=4.280344", craft))
    print(parse(input("parse("), craft))
