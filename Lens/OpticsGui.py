import FreeCAD, FreeCADGui, Part, os
from Lens import makeLens

class SingleLens:
	def Activated(self): #Initialize
		'''Add lens'''
		FreeCAD.Console.PrintMessage("Make single lens\n")
		makeLens()

	def GetResources(self):
		import OpticsPaths
		IconPath = OpticsPaths.iconsPath() + "/Lens.png"
		return {'Pixmap' : IconPath, 'MenuText': 'Create simple lens', 'ToolTip': 'Create simple lens with two surfaces'} 

FreeCADGui.addCommand('Single_Lens', SingleLens())
