#!/usr/bin/env python3
# coding: utf-8
# 
# insertLinkCmd.py


from PySide import QtGui, QtCore
import FreeCADGui as Gui
import FreeCAD as App
import Part, math, re

from libAsm4 import *


"""
    +-----------------------------------------------+
    |                  main class                   |
    +-----------------------------------------------+
"""
class insertLink( QtGui.QDialog ):
	"My tool object"

	def __init__(self):
		super(insertLink,self).__init__()

        
	def GetResources(self):
		return {"MenuText": "Insert an external Part",
				"Accel": "Ctrl+L",
				"ToolTip": "Insert an external Part from another open document",
				"Pixmap" : os.path.join( iconPath , 'LinkModel.svg')
				}


	def IsActive(self):
		if App.ActiveDocument:
			# is something selected ?
			if Gui.Selection.getSelection():
				return False
			else:
				return True
		else:
			return(False)


	def Activated(self):
		# This function is executed when the command is activated
		
		# get the current active document to avoid errors if user changes tab
		self.activeDoc = App.activeDocument()
		
		# the GUI objects are defined later down
		self.drawUI()
		
		# Search for all App::Parts in all open documents
		self.getAllParts()
		
		# build the list
		for part in self.allParts:
			newItem = QtGui.QListWidgetItem()
			newItem.setText( part.Document.Name +" -> "+ part.Name )
			newItem.setIcon(part.ViewObject.Icon)
			self.partList.addItem(newItem)

		# show the UI
		self.show()



	"""
    +-----------------------------------------------+
    |         the real stuff happens here           |
    +-----------------------------------------------+
	"""
	def onCreateLink(self):
		# parse the selected items 
		# TODO : there should only be 1
		model = []
		for selected in self.partList.selectedIndexes():
			# get the selected part
			model = self.allParts[ selected.row() ]
		# get the name of the link (as it should appear in the tree)
		linkName = self.linkNameInput.text()
		# only create link if there is a Part object and a name
		if model and linkName:
			# create the App::Link with the user-provided name
			createdLink = self.activeDoc.getObject('Model').newObject( 'App::Link', linkName )
			# assigne the user-selected model to it
			createdLink.LinkedObject = model
			# update the link
			createdLink.recompute()
			
			# close the dialog UI...
			self.close()

			# ... and launch the placement of the inserted part
			Gui.Selection.clearSelection()
			Gui.Selection.addSelection( self.activeDoc.Name, 'Model', createdLink.Name+'.' )
			Gui.runCommand( 'placeLinkCmd' )

		# if still open, close the dialog UI
		self.close()



	"""
    +-----------------------------------------------+
    |                 some functions                |
    +-----------------------------------------------+
	"""
	def getAllParts(self):
		# get all App::Part from all open documents
		self.allParts = []
		for doc in App.listDocuments().values():
			# except this document: we don't want to link to itself
			if doc != self.activeDoc:
				parts = doc.findObjects("App::Part")
				# there might be more than 1 App::Part per document
				for obj in parts:
					self.allParts.append( obj )


	def onItemClicked( self, item ):
		for selected in self.partList.selectedIndexes():
			# get the selected part
			model = self.allParts[ selected.row() ]
            # set the text of the link to be made to the document where the part is in
			self.linkNameInput.setText(model.Document.Name)


	def onCancel(self):
		self.close()



	"""
    +-----------------------------------------------+
    |     defines the UI, only static elements      |
    +-----------------------------------------------+
	"""
	def drawUI(self):

		# Our main window is a QDialog
		self.setModal(False)
		# make this dialog stay above the others, always visible
		self.setWindowFlags( QtCore.Qt.WindowStaysOnTopHint )
		self.setWindowTitle('Insert a Model')
		self.setWindowIcon( QtGui.QIcon( os.path.join( iconPath , 'FreeCad.svg' ) ) )
		self.setMinimumSize(400, 500)
		self.resize(400,500)
		#self.Layout.addWidget(self.GUIwindow)

		# label
		self.labelMain = QtGui.QLabel(self)
		self.labelMain.setText("Select Part to be inserted :")
		self.labelMain.move(10,20)
		#self.Layout.addWidget(self.labelMain)
		
		# label
		self.labelLink = QtGui.QLabel(self)
		self.labelLink.setText("Enter a Name for the link :\n(Must be unique in the Model tree)")
		self.labelLink.move(10,350)

		# Create a line that will contain the name of the link (in the tree)
		self.linkNameInput = QtGui.QLineEdit(self)
		self.linkNameInput.setMinimumSize(380, 0)
		self.linkNameInput.move(10, 400)
	
		# The part list is a QListWidget
		self.partList = QtGui.QListWidget(self)
		self.partList.move(10,50)
		self.partList.setMinimumSize(380, 280)

		# Cancel button
		self.CancelButton = QtGui.QPushButton('Cancel', self)
		self.CancelButton.setAutoDefault(False)
		self.CancelButton.move(10, 460)

		# create Link button
		self.createLinkButton = QtGui.QPushButton('Insert part', self)
		self.createLinkButton.move(285, 460)
		self.createLinkButton.setDefault(True)

		# Actions
		self.CancelButton.clicked.connect(self.onCancel)
		self.createLinkButton.clicked.connect(self.onCreateLink)
		self.partList.itemClicked.connect( self.onItemClicked)


"""
    +-----------------------------------------------+
    |       add the command to the workbench        |
    +-----------------------------------------------+
"""
Gui.addCommand( 'insertLinkCmd', insertLink() )

