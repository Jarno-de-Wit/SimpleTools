"""
A file containing multiple useful functions to aid in creating script modification scripts
"""
import sys

from .XML import XML
from .Vector import Vector

def Aircraft(name):
    #Making the XML aircraft item
    aircraft = XML(name = "Aircraft")
    #Setting all attributes for the aircraft
    aircraft["name"] = name
    aircraft["url"] = ""
    aircraft["theme"] = "Default"
    aircraft["size"] = "0,0,0"
    aircraft["boundsMin"] = "0,0,0"
    aircraft["xmlVersion"] = "6"
    aircraft["legacyJointIdentification"] = "false"
    #Create the nested XML's
    aircraft.append(Assembly(include_bodies = True))
    aircraft.append(Theme())
    return aircraft

def SubAssembly(name):
    designerparts = XML(name = "DesignerParts")
    designerparts.append(DesignerPart(name))
    return designerparts

def DesignerPart(name):
    designerpart = XML(name = "DesignerPart")
    designerpart["name"] = name
    designerpart["category"] = "Sub Assemblies"
    designerpart["icon"] = "GroupIconSubAssembly"
    designerpart["description"] = ""
    designerpart.append(Assembly())
    return designerpart

def Assembly(include_bodies = False):
    assembly = XML(name = "Assembly")
    assembly.append(Parts())
    assembly.append(Connections())
    if include_bodies:
        assembly.append(Bodies())
    return assembly

def Parts():
    #Really, just an empty XML tag
    parts = XML(name = "Parts")
    return parts

def Connections():
    connections = XML(name = "Connections")
    return connections

def Bodies():
    bodies = XML(name = "Bodies")
    return bodies


def Theme(name = "Custom"):
    theme = XML(name = "Theme")
    theme["name"] = name
    #For each of the standard material specifications, add one item to the material list
    for specification in (
        ("E9E9E9", "0.15", "0.5", "0.7"),
        ("000000", "0.3", "0.5", "0.83"),
        ("001F7F", "0.3", "0.5", "0.83"),
        ("AA2A00", "0.15", "0.5", "0.7"),
        ("3F3F3F", "0", "0.65", "0.08"),
        ("5C0000", "0", "0.65", "0.08"),
        ("FFFFFF", "0", "0.65", "0.08"),
        ("FFF0F0", "0", "0.65", "0.08"),
        ("FF0F0F", "0", "0.65", "0.08"),
        ("AAAAAA", "0", "0.65", "0.08"),
        ("3F3F3F", "0.15", "0.5", "0.7"),
        ("ABABAB", "0", "0.65", "0.08"),
        ("446677", "0", "0.65", "0.08"),
        ("FF1143", "0", "0.65", "0.08"),
        ("FF6A12", "0", "0.65", "0.08"),
        ("000000", "0", "0.65", "0.08"),
        ("FFFFFF", "0", "0.65", "0.08"),
        ("1E1E1E", "0", "0.65", "0.08"),
        ("D0D0D0", "0", "0.65", "0.08")
        ):
        theme.append(Material(*specification))
    return theme


def Material(color = "FFFFFF", r = "0", m = "0.65", s = "0.08"):
    material = XML(name = "Material")
    material["color"] = color
    material["r"] = r
    material["m"] = m
    material["s"] = s
    return material

class Info():
    """
    A class used to keep track of certain variables such as the id, to prevent overlapping id's
    """
    part_id = 0
    primaryCockpit = False
    @classmethod
    def id(cls):
        raise DeprecationWarning("Info has been deprecated. Please use init(craft)")
        cls.part_id += 1
        return f"{cls.part_id}"

    @classmethod
    def is_primary(cls):
        raise DeprecationWarning("Info has been deprecated. Please use init(craft)")
        tmp = primaryCockpit
        primaryCockpit = True
        return f"{tmp}"    

def Connection(partA, partB, nodesA = "0", nodesB = "0"):
    connection = XML(name = "Connection", format = "short")
    if isinstance(partA, XML):
        connection["partA"] = f'{partA["id"]}'
    elif isinstance(partA, int) or partA.isdigit():
        connection["partA"] = f"{partA}"
    else:
        raise ValueError("partA is not given in the expected format")
    if type(partB)  == XML:
        connection["partB"] = f'{partB["id"]}'
    elif type(partB) == int or partB.isdigit():
        connection["partB"] = f"{partB}"
    else:
        raise ValueError("partB is not given in the expected format")
    connection["attachPointsA"] = f"{nodesA}"
    connection["attachPointsB"] = f"{nodesB}"
    return connection

def Connect(partA, partB, nodesA = "0", nodesB = "0"):
    global connections
    conn = Connection(partA, partB, nodesA, nodesB)
    connections.database.append(conn)

def Meter(value):
    return value/2

def Unit(value):
    return value*2

def init(craft):
    global max_id, id_list, parts, connections
    max_id = max((int(part["id"]) for part in craft.find("Parts").database), default = 0)
    id_list = {}
    #Create shortcuts to the "Parts" and "Connections" tags
    parts = craft.find("Parts")
    connections = craft.find("Connections")

def Add_part(part):
    global parts, max_id
    max_id += 1
    part["id"] = f"{max_id}"
    parts.database.append(part)

def Copy(part):
    global max_id, id_list, parts
    new = part.deepcopy()
    max_id += 1
    new["id"] = f"{max_id}"
    if part["id"] in id_list:
        id_list[part["id"]].append(f"{max_id}")
    else:
        id_list[part["id"]] = [f"{max_id}"]
    #Add the part to the craft
    parts.database.append(new)
    return new

def Reconnect(ids, ncopies):
    global id_list, connections
    #For each existing connection (copy database to prevent accidentally
    # iterating over the newly created connections too. Even if they will all be
    # ignored (they would be), this is still needless processing.
    for conn in connections.database.copy():
        #If this connection involves any of the newly copied parts:
        if int(conn["partA"]) in ids or int(conn["partB"]) in ids:
            #For each new copy
            for i in range(ncopies):
                #Find the IDS of the parts. The new ID if this part is copied.
                # The old ID, if this part is not copied, and only the other
                # part of this connection is copied.
                idA = id_list.get(conn["partA"], conn["partA"])
                idA = idA[i] if isinstance(idA, list) else idA
                idB = id_list.get(conn["partB"], conn["partB"])
                idB = idB[i] if isinstance(idB, list) else idB
                #Create the new connection
                connections.database.append(Connection(idA, idB, conn["attachPointsA"], conn["attachPointsB"]))
        
