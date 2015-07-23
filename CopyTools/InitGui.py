import FreeCAD

class CopyToolsWorkbench (Workbench):
	"Copy Tools workbench object"
	MenuText = "Copy Tools"
	ToolTip = "Copy Tools workbench"
	Icon = FreeCAD.ConfigGet("UserAppData")  + "Mod/CopyTools/NCopy.png"
	import CopyTools
	def Initialize(self):
		#commandslist = ["copy"]
		# toolbar
		t_list = ["CopyTools_CopyVec"]
		self.appendToolbar("Copy Tools",t_list)
		# Menu
		t_list = ["CopyTools_CopyVec"]
		self.appendMenu("Copy Tools",t_list)
	#~ def GetClassName(self):
		#~ return "NCopy::Workbench"
	#~ def Activated(self):
		#~ FreeCAD.Console.PrintMessage("MyWorkbench.Activated()\n")
Gui.addWorkbench(CopyToolsWorkbench())

