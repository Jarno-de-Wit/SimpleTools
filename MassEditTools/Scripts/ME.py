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
from .IDParse import Slice, Value, ParseError
from Utils.Basics import is_int, is_float, is_vect

def Run(input_file, output_file, ids, path, mode, value, default, errout = sys.stderr):
    """
    Verifies all inputs, and runs the script if all inputs are valid.
    """
    errors, craft, output_file, ids, = \
            Verify(input_file, output_file, ids, errout = errout)

    if not path:
        print("Path is empty", file = errout)
        errors = True
    elif path.count("/") >= 2:
        print("Multi-level nested paths are not supported in the ME tool", file = errout)
        errors = True

    #Test (for command line interface only. For GUI, the DropDown already limits the options).
    if mode not in ["Set", "+=", "-=", "*=", "/=", "Append", "Prepend"]:
        print("Invalid / no operation selected", file = errout)
        errors = True

    if not value:
        print("No Value entered", file = errout)
        errors = True

    if not errors: #If all data was input correctly:
        return ME(craft, output_file, ids, path, mode, value, default, errout)
    return False


def ME(craft, output_file, ids, path, mode, value, default, errout = sys.stderr):
    """
    Mass Property Editor
    """
    parts = craft.find("Parts")

    key = path.split("/")[-1]
    for id_ in ids:
        part = parts.get_filtered("id", str(id_))
        #If there is a "/" in the path, and the value is thus inside a nested tag
        if "/" in path:
            #Find all nested tags whose name matches the path (independant of
            # the nesting depth). (Remove index from path first though if it is
            # present to prevent the path from containing indices.)
            tmp = part.find_all(path.split("/")[0].split("[")[0])
            #If any indexes are chosen, run it through the index slicer
            if "[" in path:
                tmp = Slice(tmp, tmp.split("[")[1].split("]")[0], True)
        #If the value is inside the parts' attributes, just pass in the part itself
        else:
            tmp = [part]

        #For each tag:
        for obj in tmp:
            #First run through Set, as that is not dependant on any default
            # values, nor should it be skipped if default is not given. It is
            # also not type sensitive (just directly copy the string)
            if mode == "Set":
                obj[key] = value
                continue
            #Extract the value. If it isn't present, use the default (or skip if
            # no default is given either).
            try:
                obj_val = obj[key]
            except KeyError:
                if default is None:
                    continue
                obj_val = default

            if mode == "Append":
                obj[key] = obj_val + value
                continue
            elif mode == "Prepend":
                obj[key] = value + obj_val
                continue
                
            #Now, for the data type specific actions
            if obj_val.lower() in ["true", "false"]:
                obj_val = obj_val.lower() == "true"
                if mode == "+=":
                    pass
                elif mode == "-=":
                    pass
                elif mode == "*=":
                    obj[key] = str(not obj_val).lower()
                elif mode == "\=":
                    pass
                continue
            elif (is_int(obj_val) or is_float(obj_val)) and \
                 (is_int(value) or is_float(value)):
                if mode == "+=":
                    obj[key] = str(int_float(obj_val) + int_float(value))
                elif mode == "-=":
                    obj[key] = str(int_float(obj_val) - int_float(value))
                elif mode == "*=":
                    obj[key] = str(int_float(obj_val) * int_float(value))
                elif mode == "/=":
                    try:
                        obj[key] = str(int_float(obj_val) / int_float(value))
                    except ZeroDivisionError:
                        print("Division by 0 is not allowed", file = errout)
                        return False
                continue

            #If both entries are Vectors of the same length
            elif is_vect(obj_val) and is_vect(value) and \
                 (obj_val.count(",") == value.count(",") or \
                  value.count(",") == 0):
                #If the input value is a number, make it a Vector with the same
                # length as the original value, to apply the transformation to all
                # items
                if is_int(value) or is_float(value):
                    value = int_float(value)
                else:
                    try:
                        value = Vector.from_css(value, int)
                    except ValueError:
                        value = Vector.from_css(value, float)

                try:
                    obj_val = Vector.from_css(obj_val, int)
                except ValueError:
                    obj_val = Vector.from_css(obj_val)

                if mode == "+=":
                    obj[key] = (obj_val + value).css()
                elif mode == "-=":
                    obj[key] = (obj_val - value).css()
                elif mode == "*=":
                    obj[key] = (obj_val * value).css()
                elif mode == "/=":
                    try:
                        obj[key] = (obj_val / value).css()
                    except ZeroDivisionError:
                        print("Division by 0 is not allowed", file = errout)
                        return False
                continue

            #Else, assume the values must be interpreted as Strings, because
            # they cannot be interpreted as the same non-str data type
            else:
                if mode == "+=":
                    obj[key] = obj_val + value
                elif mode == "-=":
                    obj[key] = obj_val.replace(value, "")
                elif mode == "*=":
                    if is_int(value):
                        obj[key] = int(value) * obj_val
                    else:
                        print("Cannot multiply two strings together", file = errout)
                        return False
                elif mode == "/=":
                    #/= with str is used to replace certain substrings in the
                    # string. Not because it is incredibly intuitive, but
                    # because it is a fun thing to have, and this operator was
                    # free anyway. Let me just have my fun please?
                    if "->" in value:
                        obj_str.replace(*value.split("->"))
                    else:
                        obj_str.replace(value, "")
                    obj[key] = obj_str
                continue

    #Save the final craft to the given output file
    craft.write(output_file)
    return True

def int_float(val):
    try: return int(val)
    except ValueError: return float(val)
