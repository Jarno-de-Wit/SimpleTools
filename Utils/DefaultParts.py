from .XML import XML

def Cockpit():
    """
    Creates a standard starting cockpit and returns it
    """
    #Create the cockpit
    cockpit = XML(name = "Part")
    #Set the cockpit attributes
    cockpit["id"] = "0"
    cockpit["partType"] = "Cockpit-1"
    cockpit["position"] = "0,0,0"
    cockpit["rotation"] = "0,0,0"
    cockpit["drag"] = "0,0,0,0,0,0"
    cockpit["materials"] = "7,0"
    cockpit["partCollisionResponse"] = "Default"
    #Create the Cockpit.State tag
    state = XML(name = "Cockpit.State", format = "short")
    #Set the Cockpit.State attributes
    state["primaryCockpit"] = "False"
    state["lookBackTranslation"] = "0,0"
    #Append Cockpit.State as a sub-tag to cockpit
    cockpit.append(state)
    return cockpit


def Fuselage():
    """
Creates a standard fuel tank and returns it
AttachPoints:
    0 = Back
    1 = Front

Rotated once:
positive X = front
"""
    #Create the fuselage
    fuselage = XML(name = "Part")
    #Set the fuselage attributes
    fuselage["id"] = "0"
    fuselage["partType"] = "Fuselage-Body-1"
    fuselage["position"] = "0,0,0"
    fuselage["rotation"] = "0,0,0"
    fuselage["drag"] = "0,0,0,0,0,0"
    fuselage["materials"] = "0"
    fuselage["partCollisionResponse"] = "Default"
    #Create the FuelTank.State XML tag
    fueltankstate = XML(name = "FuelTank.State", format = "short")
    #Set the FuelTank.State attributes
    fueltankstate["fuel"] = "0"
    fueltankstate["capacity"] = "0"
    #Create the Fuselage.State XML tag
    fuselagestate = XML(name = "Fuselage.State", format = "short")
    #Set the Fuselage.State attributes
    fuselagestate["version"] = "2"
    fuselagestate["frontScale"] = "1,1"
    fuselagestate["rearScale"] = "1,1"
    fuselagestate["offset"] = "0,0,2"
    fuselagestate["deadWeight"] = "0"
    fuselagestate["buoyancy"] = "0"
    fuselagestate["fuelPercentage"] = "0"
    fuselagestate["smoothFront"] = "False"
    fuselagestate["smoothBack"] = "False"
    fuselagestate["autoSizeOnConnected"] = "false"
    fuselagestate["inletSlant"] = "0"
    fuselagestate["cornerTypes"] = "2,2,2,2,2,2,2,2"
    #Append FuelTank.State and Fuselage.State to fuselage
    fuselage.append(fueltankstate)
    fuselage.append(fuselagestate)
    return fuselage

def Sphere():
    #Create the sphere
    sphere = XML(name = "Part")
    #Set the sphere attributes
    sphere["id"] = "0"
    sphere["partType"] = "Sphere-1"
    sphere["position"] = "0,0,0"
    sphere["rotation"] = "0,0,0"
    sphere["drag"] = "0,0,0,0,0,0"
    sphere["materials"] = "0"
    sphere["partCollisionResponse"] = "Default"
    #Create the ResizableShape.State XML tag
    resizableshapestate = XML("ResizableShape.State", format = "short")
    #Set the ResizableShape.State attributes
    resizableshapestate["size"] = "1"
    resizableshapestate["bounciness"] = 0
    resizableshapestate["friction"] = 1
    resizableshapestate["attachPointPosition"] = "0,-0.5,0"
    #Append ResizableShape.State to sphere
    sphere.append(resizableshapestate)
    return sphere
