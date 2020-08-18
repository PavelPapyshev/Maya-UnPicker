from PySide2 import QtCore


class UnPicker_MimeUI(QtCore.QMimeData):
	
	"""
	stores transmitted button parameters
	
	accepts arguments:
		@color[list]
	"""
	
	def __init__(self, type="button", pos="0;0", size= "0;0;1;1", color=[85,85,85], lable="", script=""):
		
		super(UnPicker_MimeUI, self).__init__()
		
		self.type = type
		self.pos = pos
		self.size = size
		self.color = color
		self.lable = lable
		self.script = script
		

#----------------------------END UnPicker_ItemRectUI