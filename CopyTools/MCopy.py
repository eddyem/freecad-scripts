# Copy objects by matrix 
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

# copy selected object S N times with offset V
def copyVec(S, N, V):
	comp = S
	if (N > 1):
		comp = S.copy()
		shape = S.copy()
		for i in range (1, N):
			shape.translate(V)
			comp = comp.fuse(shape)
	return comp
# copy selected object through a matrix
def copyMat(S, N1, N2, V1, V2):
	comp = copyVec(S, N1, V1)
	if(N2 > 1):
		comp = copyVec(comp, N2, V2)
	return comp

class MCopy:
	def __init__(self, obj, M, N, O, V1, V2):
		obj.addProperty("App::PropertyVector","Vector1","","First Vector").Vector1=V1
		obj.addProperty("App::PropertyVector","Vector2","","Second Vector").Vector2=V2
		obj.addProperty("App::PropertyInteger","N1" ,"","Number of items 1").N1=M
		obj.addProperty("App::PropertyInteger","N2" ,"","Number of items 2").N2=N
		obj.addProperty("App::PropertyLink","Source" ,"","Source shape").Source=O
		obj.Proxy = self
		obj.Shape = copyMat(O.Shape, M,N,V1,V2)
		ViewProvider(obj.ViewObject)
	def onChanged(self, fp, prop):
		if prop == "Center" or prop == "Angle" or prop == "Normal" or prop == "N" or prop == "rot":
			oldPls = fp.Shape.Placement
			self.execute(fp)
			fp.Shape.Placement = oldPls
	def execute(self, fp):
		N1 = fp.N1
		N2 = fp.N2
		V1 = fp.Vector1
		V2 = fp.Vector2
		S = fp.Source.Shape
		fp.Shape = copyMat(S, N1, N2, V1, V2)

# Copy objects to a matrix' knots, defined by vectors V1, V2 and numbers N1, N2
def makeMatrixCopy(N1=1, N2=1, V1=Base.Vector(0,0,0), V2=Base.Vector(0,0,0)):
	sel = FreeCADGui.Selection.getSelection()
	if (not sel):
		FreeCAD.Console.PrintError("Error: you should select some objects")
		QtGui.QMessageBox.critical(None,"Wrong selection","Please select a shape object")
		return None
	doc = FreeCADGui.ActiveDocument.Document
	for Obj in sel:
		rc = doc.addObject("Part::FeaturePython","MatrixCopy")
		rc.Label = Obj.Label+" (Matrix Copy)"
		MCopy(rc, N1, N2, Obj, V1, V2)
		sdoc = FreeCADGui.getDocument(Obj.Document.Name)
		sdoc.getObject(Obj.Name).Visibility=False

# A simple vector copy
def makeVectorCopy(N=1, X=0, Y=0, Z=0):
	V = Base.Vector(X,Y,Z)
	makeMatrixCopy(N1=N, V1=V)
