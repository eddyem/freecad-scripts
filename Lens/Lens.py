import FreeCAD, Part, math
import FreeCADGui
from FreeCAD import Base
from pivy import coin
# Build lens
# Radii's signs are as in optics rules: "+" when center is to the right 
# R1 - first raduis (left side)
# R2 - second radius (right side)
# d - lens width at optics axe
# H - lens height (full diameter)
# pnt = lens center
# A - optics axe direction
def makeLensApp(R1,R2,d,H, pnt, A):
	A.normalize() # make sure that this is an normalized vector
	H /= 2 # make radius from diameter
	cylh = abs(R1)+abs(R2)+d
	# Cylbeg = pnt - A*|R1|
	cylb = Base.Vector(A.x, A.y, A.z)
	cylb.multiply(abs(R1))
	cylb = pnt - cylb
	result = Part.makeCylinder(H, cylh, cylb, A)
	# Now we have base cylinder & should define its borders
	# if Rx == 0, the border will be a native cylinder border
	# otherway we should cut it by sphere
	if(R1 != 0):
		if (R1 > 0): # Center of first sphere is to the right 
			# C1 = pnt + |R1|*A
			center = Base.Vector(A.x, A.y, A.z); center.multiply(abs(R1)); center += pnt
			sphere = Part.makeSphere(abs(R1),center)
			result = result.common(sphere) # intersection
		else:
			sphere = Part.makeSphere(abs(R1),cylb)
			result = result.cut(sphere) # difference
	# Now we got a cylinder with a cut on first optical surface
	# Let's make another cut
	if(R2 != 0):
		center = Base.Vector(A.x, A.y, A.z); 
		if (R2 > 0): # Center of second sphere is to the right 
			# C2 = pnt + (|R2|+d)*A
			center.multiply(abs(R2)+d); center += pnt
			sphere = Part.makeSphere(abs(R2),center)
			result = result.cut(sphere) # intersection
		else:
			# C2 = pnt - (|R2|-d)*A
			center.multiply(abs(R2)-d); center = pnt - center
			sphere = Part.makeSphere(abs(R2),center)
			result = result.common(sphere) # difference
	return  result
#---------------------------------------------------------------------------------------------------------

class Lens:
	def __init__(self, obj, R1, R2, W, H, pnt=Base.Vector(0,0,0), A=Base.Vector(1,0,0)):
		''' Add new properties to partfeature '''
		obj.addProperty("App::PropertyFloat","Radius1","Lens","Radius1 of the lens").Radius1=R1
		obj.addProperty("App::PropertyFloat","Radius2","Lens","Radius2 of the lens").Radius2=R2
		obj.addProperty("App::PropertyLength","Width","Lens", "Width of the lens").Width=W
		obj.addProperty("App::PropertyLength","Height","Lens", "Height of the lens").Height=H
		obj.addProperty("App::PropertyVector","Setpoint","Lens", "Lens setpoint").Setpoint=pnt
		obj.addProperty("App::PropertyVector","Axe","Lens", "Optical axe direction").Axe=A
		obj.Proxy = self
		obj.Shape = makeLensApp(obj.Radius1,obj.Radius2,obj.Width,obj.Height, obj.Setpoint, obj.Axe)
		ViewProviderLens(obj.ViewObject)

	def onChanged(self, fp, prop):
		''' print changed property '''
		#FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
		if prop == "Radius1" or prop == "Radius2" or prop == "Width" or prop == "Height":
			oldPls = fp.Shape.Placement
			fp.Shape = makeLensApp(fp.Radius1, fp.Radius2, fp.Width, fp.Height, fp.Setpoint, fp.Axe)
			fp.Shape.Placement = oldPls
			ViewProviderLens(fp.ViewObject)

	def execute(self, fp):
		fp.Shape = makeLensApp(fp.Radius1,fp.Radius2,fp.Width,fp.Height, fp.Setpoint, fp.Axe)
		ViewProviderLens(fp.ViewObject)

class ViewProviderLens:
	def __init__(self, obj):
		''' Set this object to the proxy object of the actual view provider '''
		obj.Proxy = self

	def attach(self, obj):
		''' Setup the scene sub-graph of the view provider, this method is mandatory '''
		return

	def updateData(self, fp, prop):
		''' If a property of the handled feature has changed we have the chance to handle this here '''
		return

	def getDisplayModes(self,obj):
		''' Return a list of display modes. '''
		modes=[]
		return modes

	def getDefaultDisplayMode(self):
		''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
		return "Shaded"

	def setDisplayMode(self,mode):
		''' Map the display mode defined in attach with those defined in getDisplayModes.
		Since they have the same names nothing needs to be done. This method is optinal.
		'''
		return mode

	def onChanged(self, vp, prop):
		''' Print the name of the property that has changed '''
		FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

	def getIcon(self):
		Icon = """
/* XPM */
static char * Lens_xpm[] = {
"16 16 19 1",
" 	c #EDEF24",
".	c #99E879",
"+	c #8CE786",
"@	c #CEEC43",
"#	c #24DEEF",
"$	c #C2EB50",
"%	c #5FE3B3",
"&	c #47E1CC",
"*	c #E0EE32",
"=	c #D7ED3A",
"-	c #000000",
";	c #A4E96D",
">	c #7FE693",
",	c #6DE4A5",
"'	c #52E2C1",
")	c #32DFE1",
"!	c #2ADFE9",
"~	c #26DEED",
"{	c #42E1D1",
"       .+       ",
"      @##$      ",
"      %##&      ",
"     *####=     ",
"--------##;     ",
"     >##--,     ",
"     '####--    ",
"     )####! --  ",
"     ~####!   --",
"     )####{  -- ",
"     '####,--   ",
"     >###--     ",
"---------#=     ",
"     *###&      ",
"      %##$      ",
"      @#+       "};
			"""
		return Icon

	def __getstate__(self):
		''' When saving the document this object gets stored using Python's cPickle module.
		Since we have some un-pickable here -- the Coin stuff -- we must define this method
		to return a tuple of all pickable objects or None.
		'''
		return None

	def __setstate__(self,state):
		''' When restoring the pickled object from document we have the chance to set some
		internals here. Since no data were pickled nothing needs to be done here.
		'''
		return None

# make one lens with parameters R1, R2, W, H, pointed @ pnt with axe A
def makeLens(R1=15.0, R2=-15., W=1., H=7., pnt=Base.Vector(0,0,0), A=Base.Vector(1,0,0)):
	a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython","Lens")
	Lens(a, R1, R2, W, H, pnt, A)
	ViewProviderLens(a.ViewObject)
	a.ViewObject.ShapeColor = (0.7,0.7,0.85)
	a.ViewObject.Transparency = 80
	return a

# make several lens started at pnt0 with axe A
# LDescr - array of [R1, R2, W, H, D] for each lens
# D is ditance between subsequent surfaces
def makeLensBench(LDescr, pnt0=Base.Vector(0,0,0), A=Base.Vector(1,0,0)):
	is_array = lambda var: isinstance(var, (list, tuple))
	if (not is_array(LDescr)):
		FreeCAD.Console.PrintError("Wrong input! LDescr is array of arrays [R1, R2, W, H, D]\n")
		return
	A.normalize()
	pnt = Base.Vector(pnt0.x, pnt0.y, pnt0.z)
	if(not is_array(LDescr[0])): # only one lens, parameters in single array
		LDescr = [LDescr]
	# make a group to simpify lens' management
	doc = FreeCAD.activeDocument()
	grp = doc.addObject("App::DocumentObjectGroup", "LensBench")
	for Descr in LDescr:
		D = 0. # make default value to be on the safe side
		try: # make try..catch for a case of omitted parameters
			R1=Descr[0]; R2=Descr[1]; W=Descr[2]; H=Descr[3]; D=Descr[4]
		except:
			pass
		l = makeLens(R1,R2,W,H,pnt,A) # create a successive lens
		grp.addObject(l)
		delta = Base.Vector(A.x, A.y, A.z).multiply(D+W)
		FreeCAD.Console.PrintMessage("d = ("+str(delta.x)+","+str(delta.y)+","+str(delta.z)+")\n")
		pnt += delta # go to next lens
		FreeCAD.Console.PrintMessage("lens done! pnt0 = ("+str(pnt.x)+","+str(pnt.y)+","+str(pnt.z)+")\n")
	return grp
