from PySide2 import QtCore, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as mui


def maya_main_window():
    main_window_ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class testWindow(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(Window, self).__init__(parent)
        
        self.setWindowTitle("Test Window")
        self.setMinimumWidth(200)
        self.setMinimumHeight(50)
        
        # get rid of help button for windows
        self.setWindowFlags(
            self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        
        
if __name__ == "__main__":
    
    d = testWindow()
    d.show()