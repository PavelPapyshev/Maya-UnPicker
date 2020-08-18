

class UnPicker_MigratoryData(object):
	
	"""
	stores write/read data of a node
	"""
	
	def __init__(self):
		
		super(UnPicker_MigratoryData, self).__init__()
		
		self.widgetType = []
		self.widgetPos = []
		self.widgetWidthHeight = []
		self.widgetColor = []
		self.widgetLabel = []
		self.widgetScript = []


	def getCountItem(self):
		
		return len(self.widgetType)
		
#--------------------------------------------	
	
	def addWidgetType(self, type=None):
		
		self.widgetType.append(type)
	
	
	def getWidgetType(self):
		
		return self.widgetType
#--------------------------------------------		
	
	def addWidgetPos(self, pos=None):
		
		self.widgetPos.append(pos)
	
	
	def getWidgetPos(self):
		
		return self.widgetPos
#--------------------------------------------			
	
	def addWidgetWidthHeight(self, size=None):
		
		self.widgetWidthHeight.append(size)
	
	
	def getWidgetWidthHeight(self):
		
		return self.widgetWidthHeight
#--------------------------------------------

	def addWidgetColor(self, color=None):
			
		self.widgetColor.append(color)
	
	
	def getWidgetColor(self):
		
		return self.widgetColor
#--------------------------------------------

	def addWidgetLabel(self, label=None):
		
		self.widgetLabel.append(label)
	
	
	def getWidgetLabel(self):
		
		return self.widgetLabel
#--------------------------------------------	

	def addWidgetScript(self, script=None):
		
		self.widgetScript.append(script)
	
	
	def getWidgetScript(self):
		
		return self.widgetScript
#--------------------------------------------	

#----------------------------END UnPicker_MigratoryData	