# Maya-UnPicker

For Autodesk Maya.

UnPicker (universal picker) - a script for quickly selecting objects in the scene.

 - Supports working with multiple characters by switching between them.
 
 - It is possible to work with multiple tabs (create and delete).
 
 - It is possible to upload images as a background.
 
 - The script works in two modes: placing and changing the properties of buttons and direct selection of objects in the scene using the placed buttons.
 
 - The script allows you to interactively place, move, resize, color, label and performed button action.
 
 - If objects are selected in the scene, then when placing the button will be automatically the text of the script for selecting these objects has been formed; this text can be edited.
 
 - It is possible to delete and duplicate buttons (if objects are selected in the scene,
then when duplicated, it will generate the text of the script for selecting these objects, otherwise the text of the parent button will be duplicated).
 
 - All information is saved in the attributes of the node, so remember to save the entire scene.
 
 - It is possible to add and remove button presets that are saved to a json file.
 
 Place the project in the script folder. For start:
 ```python
import UnPicker.UnPicker_Main as UnPicker 
UnPicker.UnPicker_Main()
 ```
