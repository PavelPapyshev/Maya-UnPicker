import maya.cmds as mc
from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from UI.UnPicker_MainWindowUI import UnPicker_MainWindowUI


def UnPicker_Main():

	"""
	Script run
	"""
	
	#if the window already exists, delete
	if mc.workspaceControl("MainWindowUnPickerUIWorkspaceControl", exists=1):
		mc.deleteUI("MainWindowUnPickerUIWorkspaceControl", control = 1)
		mc.workspaceControlState("MainWindowUnPickerUIWorkspaceControl", remove=1)
	
	#if settings remain in memory, clear
	if mc.workspaceControl("ItemOptionsWindowUnPickerUIWorkspaceControl", exists=1):
		mc.deleteUI("ItemOptionsWindowUnPickerUIWorkspaceControl", control = 1)
		mc.workspaceControlState("ItemOptionsWindowUnPickerUIWorkspaceControl", remove=1)
	
	#create mainWindow
	mainWindow = UnPicker_MainWindowUI()
	mainWindow.show(dockable=1, area="right", allowedArea="right", floating=1)
	
	mc.workspaceControl("MainWindowUnPickerUIWorkspaceControl",
						label="Universal Picker",
						edit=1,
						tabToControl=["AttributeEditor", -1])