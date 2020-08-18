import maya.cmds as mc
import re
import os
import json


#global variables
UnPicker_EditMode = False
UnPicker_NameSpace = ""
UnPicker_PressShift = False


def getNodeNameComposition(nameNode):

	"""
	splits the full node name into NameSpace and short name
	
	accepts arguments:
		@nameNode[str] - full name
		
	return arguments:
		@nameSpace[str] - NameSpace
		@name[str] - short name
	"""
	
	nameNode = nameNode.split("|")[-1]
	
	formula = re.compile("^(.*):?UnPicker_(.*)\Z")
	result = formula.match(nameNode)
	
	nameSpace = result.group(1)
	nameSpace = nameSpace.split(":")[0]
	
	name = result.group(2)
	
	return nameSpace, name

	
def imageSearch(imagePath):

	"""
	if the image is not found in the specified path, search for it in the project directory
	
	accepts arguments:
		@imagePath[str]
	
	return arguments:
		@[str]
	"""
	
	if os.path.exists(imagePath):
		return imagePath
	
	img = os.path.basename(imagePath)
	imgDir = os.path.join(os.path.dirname(__file__), "image")
	
	#if the problem is with the encoding, then return the original path
	try:
		img = os.path.join(imgDir, img)
	except:
		return imagePath
	
	if os.path.exists(img):
		return img
	
	else:
		return imagePath
	

def getImagePath():
		
	"""
	returns the path to the image

	return arguments:
		@imagePath[str]
	"""

	imagePath = openLoadFileDialog("Open Image")

	if imagePath:
		imagePath = imagePath[0]

	else:
		imagePath = ""

	return imagePath
			
	
def openLoadFileDialog(captionDialog=""):

	"""
	opens a file selection dialog box
	
	return arguments:
		@[str] - the path to the file
	"""
	
	return mc.fileDialog2(dialogStyle=2, fileMode=1, caption=captionDialog, okCaption="Open")

	
def getEnterRGB(rgb):
		
	"""
	returns color when the cursor is over an object

	accepts arguments:
		@rgb[list]

	return arguments:
		@rgbNew[list]
	"""

	rgbNew = []

	for color in rgb:
		newColor = color + .35

		if newColor > 1:
			newColor = color - .35

		rgbNew.append(newColor)

	return rgbNew
		

def loadItemsOptions():
	
	"""
	loads button presets
		
	return arguments:
		@data[list]
	"""
	
	try: 
		#the path to the file
		path = os.path.join(os.path.dirname(__file__), "ItemsOptions.json")
		
		#checking for an empty path
		if not os.path.exists(path):
			return
		
		with open(path, "r") as loadFile:
			data = json.load(loadFile)
		
		return data
	
	except:
		return

		
def saveItemsOptions(data):
	
	"""
	saves button presets
	
	accepts arguments:
		@data[list]
	"""
	
	#the path to the file
	path = os.path.join(os.path.dirname(__file__), "ItemsOptions.json")
	
	#write to file
	with open(path, "w") as saveFile:
		json.dump(data, saveFile, indent=4)
		
