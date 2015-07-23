import FreeCAD, FreeCADGui, os
def modulePath():
    """returns the current Optics design module path @return Module path"""
    path1 = FreeCAD.ConfigGet("AppHomePath") + "Mod/Lens"
    path2 = FreeCAD.ConfigGet("UserAppData") + "Mod/Lens"
    if os.path.exists(path2):
        return path2
    else:
        return path1

def iconsPath():
    """returns the current Optics design module icons path @return Icons path"""
    path = modulePath()
    return path
