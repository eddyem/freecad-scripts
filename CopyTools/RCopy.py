# Copy objects by circular trajectory
import math
from PyQt4 import QtGui
import FreeCAD, FreeCADGui, Part
from FreeCAD import Base

class ViewProvider:
	def __init__(self, obj):
		obj.Proxy = self
	def getDisplayModes(self,obj):
		''' Return a list of display modes. '''
		modes=[]
		return modes
	def getDefaultDisplayMode(self):
		''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
		return "Shaded"
	#~ def getIcon(self):
		#~ Icon = """
#/* XPM */
#static char * icon_xpm[] = {
#~ "      @#+       "};
			#~ """
		#~ return Icon

# copy selected objects along circle
# C - center of circle
# A - normal to the circle
# Ang - angle between copies
# N - number of copies (N=0 - full circle), N <= 360/Ang
# rot == False - copy selection without rotating
# moveOriToGrp == True if you want to put original into group
def copyCirc(S, C, A, Ang, N, rot):
	comp = S
	if (N == 0):
		N = int(360./math.fabs(Ang))
	#if (N > 1):
	comp = S.copy()
	#comp.rotate(C, A, Ang)
	#if (not rot):
	#	comp.rotate(comp.Placement.Base, A, -(Ang))
	for i in range (1, N):
		shape = S.copy()
		shape.rotate(C, A, Ang*i)
		if (not rot):
			shape.rotate(shape.Placement.Base, A, -(Ang*i))
		comp = comp.fuse(shape)
	return comp

class RCopy:
	def __init__(self, obj, C,A,N,S,n,r):
		obj.addProperty("App::PropertyVector","Center","","Center").Center=C
		obj.addProperty("App::PropertyAngle","Angle" ,"","Angle").Angle=A
		obj.addProperty("App::PropertyVector","Normal" ,"","Normal to circle").Normal=N
		obj.addProperty("App::PropertyLink","Source" ,"","Source shape").Source=S
		obj.addProperty("App::PropertyInteger","N" ,"","Number of items").N=n
		obj.addProperty("App::PropertyBool","rot" ,"","Rotate objects").rot=r
		obj.Proxy = self
		obj.Shape = copyCirc(S.Shape, C, N, A, n, r)
		ViewProvider(obj.ViewObject)
	def onChanged(self, fp, prop):
		if prop == "Center" or prop == "Angle" or prop == "Normal" or prop == "N" or prop == "rot":
			Anga = math.fabs(fp.Angle)
			Sign = fp.Angle / Anga
			Anga %= 360
			n = fp.N
			if (n > (360./Anga+1) or n < 0 or (n > 360./Anga and Anga < 180.)):
				fp.N = int(360./Anga)
				return
			if (fp.Angle != Anga * Sign):
				fp.Angle = Anga * Sign
				return
			oldPls = fp.Shape.Placement
			self.execute(fp)
			fp.Shape.Placement = oldPls
			#ViewProvider(obj.ViewObject)
	def execute(self, fp):
		S = fp.Source.Shape
		C = fp.Center
		N = fp.Normal
		A = fp.Angle
		n = fp.N
		r = fp.rot
		fp.Shape = copyCirc(S, C, N, A, n, r)
		#ViewProvider(obj.ViewObject)

def makeRadialCopy(Center=Base.Vector(0,0,0), Angle=90, Normal=Base.Vector(0,0,1), N=4, rot=True):
	sel = FreeCADGui.Selection.getSelection()
	if (not sel):
		FreeCAD.Console.PrintError("Error: you should select some objects")
		QtGui.QMessageBox.critical(None,"Wrong selection","Please select a shape object")
		return None
	doc = FreeCADGui.ActiveDocument.Document
	for Obj in sel:
		rc = doc.addObject("Part::FeaturePython","RadialCopy")
		rc.Label = Obj.Label+" (Radial Copy)"
		RCopy(rc, Center, Angle, Normal, Obj, N, rot)
		sdoc = FreeCADGui.getDocument(Obj.Document.Name)
		sdoc.getObject(Obj.Name).Visibility=False
		#rc.ViewObject.Proxy=0
