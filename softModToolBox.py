from maya import cmds, mel
import re
import maya.OpenMayaUI as mui
from PyQt4 import QtCore, QtGui
import sip

''' --- Utils --- '''
import softModToolBox_utils as smtbUtils
reload(smtbUtils)
''' --- Utils --- '''


def getMayaWindow():
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)
    
def main():
    global dialog
    
    try:
    	dialog.close()
    except:
        pass
    
    dialog = SoftModToolBox()
    dialog.show()
    
    

class SoftModToolBox(QtGui.QDialog):
    #
    def __init__(self, parent=getMayaWindow()):
        super(SoftModToolBox, self).__init__(parent)
        
        
        # Window infos
        self.setObjectName("SoftModToolBoxTiti")
        self.setWindowTitle("Sliding SoftMod UI")
        
        
        # PanelLayout for outliner
        paneLayoutName = cmds.paneLayout()
        ptr            = mui.MQtUtil.findControl(paneLayoutName) # Find a pointer to the paneLayout that we just created
        paneLayout     = sip.wrapinstance(long(ptr), QtCore.QObject) # Wrap the pointer into a python QObject
        
        
        # Widgets
            # ComboBox
        filtersCBTitle = QtGui.QLabel("Filters :")
        self.filtersCB = QtGui.QComboBox(parent=self)
        self.filtersCB.addItems(["softMod", "joint", "mesh", "light", "objectSet", ""])
            # Outliner
        self.outlinerName = cmds.outlinerEditor(panel=paneLayoutName, showShapes = True, showDagOnly = False)
        ptr               = mui.MQtUtil.findControl(self.outlinerName)
        outliner          = sip.wrapinstance(long(ptr), QtCore.QObject)
        self.updateOutliner()
            # Buttons
        bpmBtn   = QtGui.QPushButton("Make BPM Deformer", parent=self)
        slideBtn = QtGui.QPushButton("Make Sliding SoftMod", parent=self)
        closeBtn = QtGui.QPushButton("Close UI", parent=self)
            # Widgets size
        self.filtersCB.setMaximumWidth(1000)
        bpmBtn.setMaximumWidth(1000)
        slideBtn.setMaximumWidth(1000)
        closeBtn.setFixedHeight(25)
        
        
        # Widgets position
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        
        grid.addWidget(filtersCBTitle, 1, 0)
        grid.addWidget(self.filtersCB, 1, 1, 1, 9)
        
        grid.addWidget(outliner, 2, 0, 5, 0)
        
        grid.addWidget(bpmBtn, 7, 5, 1, 5)
        grid.addWidget(slideBtn, 8, 5, 1, 5)
        grid.addWidget(closeBtn, 7, 0, 2, 5)
        #grid.addWidget(bpmBtn, 7, 0, 1, 5)
        #grid.addWidget(slideBtn, 8, 0, 1, 5)
        #grid.addWidget(closeBtn, 7, 5, 2, 5)
        
        self.setLayout(grid)
        self.setGeometry(250, 350, 250, 350)
        
        
        # Signals connection
        self.filtersCB.currentIndexChanged.connect(self.updateOutliner)
        bpmBtn.clicked.connect(smtbUtils.do_softModBpm) #self.connect(bpmBtn, QtCore.SIGNAL("clicked()"), do_softModBpm)
        slideBtn.clicked.connect(smtbUtils.do_softModCtrl) #self.connect(slideBtn, QtCore.SIGNAL("clicked()"), do_softModCtrl)
        #closeBtn.clicked.connect(self.close)
        closeBtn.clicked.connect(self.close) 
        
        
    #
    def updateOutliner(self):
        inputList  = cmds.selectionConnection(worldList=True)
        fromEditor = cmds.selectionConnection(activeList=True)
        
        CBcurrText = self.filtersCB.currentText()
        
        filterItem = cmds.itemFilter(byType = str(CBcurrText))
        
        cmds.outlinerEditor(self.outlinerName, edit=True, mainListConnection=inputList, filter=filterItem)
        cmds.outlinerEditor(self.outlinerName, edit=True, selectionConnection=fromEditor)
        
        
        
##########
def buildUI():
	if __name__ == "softModToolBox": #'__main__'
		main()
	
	'''if cmds.window("FormExample", q=True, exists=True):
		cmds.deleteUI("FormExample")
	cmds.window("FormExample")
	cmds.columnLayout()
	cmds.button(label="My Button", command='smtbUtils.do_softModBpm()')
	cmds.window("FormExample", visible=True, e=True)

	win = FormExample()'''
