import FreeCAD, FreeCADGui, Part
import math
from FreeCAD import Base

def CopyObj(obj, NMsuff = ""):
	name = obj.Name
	shape = obj.Shape
	newshape = shape.copy()
	t = obj.Type
	newobject = FreeCAD.ActiveDocument.addObject(t,name)
	for p in s.PropertiesList:
		newobject.getPropertyByName(p) = obj.getPropertyByName(p)
	newobject.Shape = newshape
	colr = FreeCADGui.activeDocument().getObject(obj.Name).ShapeColor
	FreeCADGui.activeDocument().getObject(newobject.Name).ShapeColor = colr
	#newobject.ShapeColor = sel.ShapeColor
	newobject.Label = obj.Label + NMsuff
	return newobject

# if toGRP == True, move copies to group
# if itself == True, object changed itself
def transformObj(mat, toGRP=False, itself=False, NMsuff=""): 
	sel = FreeCADGui.Selection.getSelection()
	if sel:
		if(toGRP):
			doc = FreeCAD.activeDocument()
			grp = doc.addObject("App::DocumentObjectGroup", "Scaling")
		for Obj in sel:
			if(not itself):
				newobject = CopyObj(Obj, NMsuff)
			else:
				newobject = Obj
			newobject.Shape = newobject.Shape.transformGeometry(mat)
			if(toGRP):
				grp.addObject(newobject)
	else:
		FreeCAD.Console.PrintError("Error: you should select some objects")

# scales selected object[s] into copies
def scale(N, toGRP=False, itself=False):
	mat = Base.Matrix()
	mat.scale(Base.Vector(N,N,N))
	transformObj(mat, toGRP, itself, "scaled")


# rotates selected object[s] (angles X,Y,Z) into copies
# !!! first - rotate X, then - Y, last - Z
def rotXYZ(X,Y,Z, Center=None, toGRP=False, itself=False):
	sel = FreeCADGui.Selection.getSelection()
	if sel:
		if(toGRP):
			doc = FreeCAD.activeDocument()
			grp = doc.addObject("App::DocumentObjectGroup", "Rotating")
		for Obj in sel:
			if(not itself):
				newobject = CopyObj(Obj, "rotated")
			else:
				newobject = Obj
			S = newobject.Shape
			if(Center == None):
				try:
					Center = S.CenterOfMass
				except:
					Center = Base.Vector(0,0,0)
			S.rotate(Center, Base.Vector(1,0,0), X)
			S.rotate(Center, Base.Vector(0,1,0), Y)
			S.rotate(Center, Base.Vector(0,0,1), Z)
			if(toGRP):
				grp.addObject(newobject)
	else:
		FreeCAD.Console.PrintError("Error: you should select some objects")

def moveXYZ(X,Y,Z, toGRP=False, itself=False):
	sel = FreeCADGui.Selection.getSelection()
	if sel:
		if(toGRP):
			doc = FreeCAD.activeDocument()
			grp = doc.addObject("App::DocumentObjectGroup", "Scaling")
		for Obj in sel:
			if(not itself):
				newobject = CopyObj(Obj, "translated")
			else:
				newobject = Obj
			newobject.Shape.translate(Base.Vector(X,Y,Z))
			if(toGRP):
				grp.addObject(newobject)
	else:
		FreeCAD.Console.PrintError("Error: you should select some objects")

# N - number of teeth, norm - normal to gear
def cutNteeth(N, norm=Base.Vector(0,0,1)):
	sel = FreeCADGui.Selection.getSelection()
	def prErr():
		FreeCAD.Console.PrintError("Error: you should select two objects\n")
	if (not sel):
		prErr(); return None
	L = len(sel)
	if(L != 2):
		prErr(); return None
	if(N < 2):
		FreeCAD.Console.PrintError("Error: N shold be more than 1\n"); return None
	aBase = sel[0]
	Tooth = sel[1]
	try:
		Center = aBase.Shape.CenterOfMass
	except:
		Center = Base.Vector(0,0,0)
	ang = 360./N
	try:
		for i in range(1, N+1):
			aBase.Shape = aBase.Shape.cut(Tooth.Shape)
			Tooth.Shape.rotate(Center, norm, ang)
			FreeCAD.Console.PrintError(i+"\n")
	except:
		FreeCAD.Console.PrintError("Error: bad selection\n")
		return None
		

