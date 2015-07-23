class OpticsWorkbench ( Workbench ):
	 """ @brief Workbench of Optics design module. Here toolbars & icons are append. """
	 import OpticsPaths
	 import OpticsGui 

	 Icon = OpticsPaths.iconsPath() + "/Ico.png"
	 MenuText = "Optics design module"
	 ToolTip = "Optics design module" 

	 def Initialize(self):
		# ToolBar
		list = ["Optics_Lens"]
		self.appendToolbar("OpticTools",list)

		# Menu
		list = ["Optics_Lens"]
		self.appendMenu("Optics design",list)
Gui.addWorkbench(OpticsWorkbench())
