import math
from PyQt4 import QtGui
import FreeCAD, FreeCADGui, Part
from FreeCAD import Base

from RCopy import makeRadialCopy
from MCopy import makeVectorCopy, makeMatrixCopy


# Copy 1 object N times by selected trajectory (BSpline)
# Trajectory should be first selection, all other - a copying objects
# original object should not be at beginning of trajectory
def copyByTrajectory(N=4):
	sel = FreeCADGui.Selection.getSelection()
	def prErr():
		FreeCAD.Console.PrintError("Error: you should select a traectory and one object\n")
	if (not sel):
		prErr(); return None
	L = len(sel)
	if(L != 2):
		prErr(); return None
	if(N < 2):
		FreeCAD.Console.PrintError("Error: N shold be more than 1\n"); return None
	Traj = sel[0].Shape
	#(a, b) = Traj.ParameterRange
	Obj = sel[1]
	TLen = Traj.Length / (N - 1)
	curPos = 0
	doc = FreeCAD.activeDocument()
	grp = doc.addObject("App::DocumentObjectGroup", "BSplineCopy")
	try:
		for i in range(0, N):
			v = Traj.valueAt(curPos); curPos += TLen
			newobj = CopyObjAt(Obj, v)
			grp.addObject(newobj)
	except:
		FreeCAD.Console.PrintError("Error: bad selection\n")
		return None
		


