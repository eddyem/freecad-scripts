import FreeCAD, FreeCADGui
from NCopy import copyVec
from FreeCAD import Base

class _CopyVec:
	"Copy selected object[s] N times along vector"
	def IsActive(self):
		if len(FreeCADGui.Selection.getSelection()) > 0:
			return True
		else:
			return False

	def Activated(self):
		"Multiple copy by vector"
		#~ from getGUIparams import getNparametersFromWindow as getWinPars
		from getGUIparams import runner as getWinPars
		from getGUIparams import allvals as L
		FreeCAD.Console.PrintMessage("CopyVec activated!\n")
		getWinPars(["a","b","c","d"])
		is_array = lambda var: isinstance(var, (list, tuple))
		if (is_array(L) and len(L) != 4):
			return
		try:
			N = int(L[0].text())
			dx = float(L[1].text())
			dy = float(L[2].text())
			dz = float(L[3].text())
		except:
			FreeCAD.Console.PrintError("Wrong input! Only numbers allowed...\n")
		else:
			copyVec(N, Base.Vector(dx,dy,dz))

	def GetResources(self):
		IconPath = FreeCAD.ConfigGet("UserAppData")  + "Mod/CopyTools/NCopy.png"
		return {'Pixmap' : IconPath, 'MenuText': 'Copy Vec', 'ToolTip': 'Copy selected objects N times by given vector'} 

FreeCADGui.addCommand('CopyTools_CopyVec', _CopyVec())
