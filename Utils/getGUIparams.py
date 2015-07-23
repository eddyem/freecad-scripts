#!/usr/bin/python
# coding: koi8-r

import sys
import pygtk
pygtk.require('2.0')
import gtk
#import FreeCAD, FreeCADGui

allvals = []

class MyWin:
	def __init__(self, labels, title):
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title(title)
		window.connect("destroy", self.delete_event)
		vbox = gtk.VBox(False, 5)
		window.add(vbox)
		self.edits = []
		for label in labels:
			box = gtk.HBox(False, 5)
			vbox.pack_start(box, True, True, 0)
			edit = gtk.Entry()
			glabel = gtk.Label(label)
			box.pack_start(glabel, False, False, 0)
			box.pack_end(edit, True, True, 0)
			self.edits.append(edit)
		box = gtk.HBox(False, 5)
		vbox.pack_start(box, True, True, 0)
		button = gtk.Button("OK")
		button.connect("clicked", self.ok)
		box.pack_start(button, False, False, 0)
		button = gtk.Button("Cancel")
		button.connect("clicked", self.no)
		box.pack_start(button, True, True, 0)
		window.show_all()
	def ok(self, widget):
		print "O.K.!"
		global allvals
		for e in self.edits:
			value = e.get_text()
			if value:
				allvals.append(value)
 		gtk.main_quit()
	def no(self, widget):
		print "Cancel!"
		gtk.main_quit()
	def delete_event(self, widget):
		gtk.main_quit()

class runner:
	def __init__(self, alllab, atitle='Title'):
		MyWin(labels=alllab, title=atitle)
		gtk.main()

#~ def getNparametersFromWindow(labels, title='Title'):
	#~ MyWin(labels, title)
	#~ gtk.main()


#~ # Returns a list of strings or empty list if user cancel's
#~ def getNparametersFromWindow(labels, title='Tell me more'):
	#~ def callback(self, widget, data=None):
		#~ print "Hello again - %s was pressed" % data
	#~ def delete_event(self, widget, event, data=None):
		#~ gtk.main_quit()
		#~ return False
	#~ def __init__(self):
		#~ window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		#~ window.set_title("Table")
		#~ window.connect("delete_event", delete_event)
		#~ vbox = gtk.VBox(False, 5)
		#~ window.add(vbox)
		#~ box.show()
		#~ for label in labels:
			#~ box = gtk.HBox(False, 5)
			#~ vbox.pack_start(box, True, True, 0)
			#~ box.show()
			#~ edit = gtk.Entry()
			#~ glabel = gtk.Label(label)
			#~ box.pack_start(glabel, False, False, 0)
			#~ box2.pack_start(edit, True, True, 0)
			#~ edits.append(edit)
		#~ box = gtk.HBox(False, 5)
		#~ vbox.pack_start(box, True, True, 0)
		#~ box.show()
		#~ button = gtk.Button("OK")
		#~ button.connect("clicked", callback, "OK")
		#~ box.pack_start(button, False, False, 0)
		#~ button.show()
		#~ button = gtk.Button("Cancel")
		#~ button.connect("clicked", self.callback, "Cancel")
		#~ box.pack_start(button, True, True, 0)
		#~ button.show()
		#~ window.show()





#~ import sys
#~ from PyQt4 import QtGui, QtCore
#~ import FreeCAD, FreeCADGui
#~ 
#~ appcode = -1
#~ 
#~ # Returns a list of strings or empty list if user cancel's
#~ def getNparametersFromWindow(labels, title='Tell me more'):
	#~ global appcode
	#~ app = QtGui.QApplication(sys.argv)
	#~ form = QtGui.QFormLayout()
	#~ edits = []
	#~ for label in labels:
		#~ edit = QtGui.QLineEdit() # ++ QSpinBox & QDoubleSpinBox
		#~ form.addRow(label, edit)
		#~ edits.append(edit)
	#~ buttons = QtGui.QDialogButtonBox()
	#~ buttons.setOrientation(QtCore.Qt.Horizontal)
	#~ buttons.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
	#~ layout = QtGui.QVBoxLayout()
	#~ layout.addLayout(form)
	#~ layout.addWidget(buttons)
#~ 
	#~ global success
	#~ success = False
	#~ FreeCAD.Console.PrintMessage("one\n")
	#~ def ok(): 
		#~ global success
		#~ FreeCAD.Console.PrintMessage("OK\n")
		#~ success = True
		#~ w.close() 
	#~ def cancel():
		#~ global success
		#~ FreeCAD.Console.PrintMessage("Cancel\n")
		#~ success = False
		#~ w.close()
	#~ FreeCAD.Console.PrintMessage("two\n")
	#~ QtCore.QObject.connect(buttons, QtCore.SIGNAL("accepted()"), ok);
	#~ QtCore.QObject.connect(buttons, QtCore.SIGNAL("rejected()"), cancel);
	#~ FreeCAD.Console.PrintMessage("three\n")
	#~ w = QtGui.QDialog()
	#~ w.setWindowTitle(title)
	#~ w.setLayout(layout)
	#~ FreeCAD.Console.PrintMessage("four\n")
	#~ QtCore.QMetaObject.connectSlotsByName(w)
	#~ w.show()
	#~ appcode = app.exec_()
	#~ while (appcode == -1):
		#~ pass
	#~ FreeCAD.Console.PrintMessage("five\n")
	#~ if success:
		#~ FreeCAD.Console.PrintMessage("ret\n")
		#~ return edits
	#~ FreeCAD.Console.PrintMessage("none\n")
	#~ return []




#~ from PyQt4 import QtGui,QtCore
#~ 
#~ # Get N parameters from dialog window
#~ #	Labels - an array with parameters' labels
#~ #	Parameters - output array of string values
#~ # 	proceed - a procceeding function (when OK is pressed)
#~ # 	Title - window title
#~ def getNparametersFromWindow(Labels, Title="Tell me more"):
	#~ RET = 0
	#~ Parameters = []
	#~ def hide():
		#~ RET = 1
		#~ del Parameters[:]
		#~ dialog.hide()
	#~ def proceed():
		#~ RET = 1
		#~ dialog.hide()
	#~ dialog = QtGui.QDialog()
#~ #	dialog.resize(200,300)
	#~ dialog.setWindowTitle(Title)
	#~ la = QtGui.QVBoxLayout(dialog)
	#~ lbl = []
	#~ for i in range(0, len(Labels)):
		#~ lbl.append(QtGui.QLabel(Labels[i]))
		#~ la.addWidget(lbl[i])
		#~ Parameters.append(QtGui.QLineEdit())
		#~ la.addWidget(Parameters[i])
	#~ okbox = QtGui.QDialogButtonBox(dialog)
	#~ okbox.setOrientation(QtCore.Qt.Horizontal)
	#~ okbox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
	#~ la.addWidget(okbox)
	#~ QtCore.QObject.connect(okbox, QtCore.SIGNAL("accepted()"), proceed)
	#~ QtCore.QObject.connect(okbox, QtCore.SIGNAL("rejected()"), hide)
	#~ QtCore.QMetaObject.connectSlotsByName(dialog)
	#~ dialog.show()
	#~ while (RET != 1):
		#~ pass
	#~ return Parameters

