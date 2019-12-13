import maya.cmds as cmds
import maya.mel as mel
from PySide2 import QtGui,QtCore,QtWidgets
import  maya.OpenMayaUI as omui
from shiboken2 import wrapInstance as wrp
import pymel.core.datatypes as dt



class ErrorUI(QtWidgets.QWidget):

    def __init__(self, parent = None):
        super(ErrorUI, self).__init__(parent)
        self.setWindowTitle('Check Symmetry')
        self.setWindowFlags(QtCore.Qt.Window)
        self.lay_main = QtWidgets.QVBoxLayout(self)
        self.label_error = QtWidgets.QLabel('Not symmetrical')
        self.lay_main.addWidget(self.label_error)



def CheckSym():
    mel.eval('ConvertSelectionToVertices')
    select = cmds.ls(sl=True, fl=True)
    symmetry = 0
    posList = []
    for p in select:
        posList.append(dt.Vector(cmds.xform(p, q=1, ws=1, t=1)))

    print posList

    cx = sum([vec.x for vec in posList]) / len(posList)
    cy = sum([vec.y for vec in posList]) / len(posList)
    cz = sum([vec.z for vec in posList]) / len(posList)

    # center = dt.Vector(cx, cy, cz)

    X = [vec.x for vec in posList]
    print X
    Y = [vec.y for vec in posList]
    print Y
    Z = [vec.z for vec in posList]
    print Z

    PlusX = []
    MinusX = []
    for x in X:
        if x > cx:
            mX = x - cx
            PlusX.append(mX)
        else:
            mY = cy - x
            MinusX.append(mX)

    print PlusX
    print MinusX

    for y in Y:
        for z in Z:
            for px in PlusX:
                PX = px - cx
                FV = dt.Vector(PX, y, z)
                for mx in MinusX:
                    MX = cx - mx
                    SV = dt.Vector(MX, y, z)
                    if FV == SV:
                        symmetry += 1
                    else:
                        windowE()
                        return False

    if symmetry == len(posList):
        windowC()

def getMayaWindow():
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrp(long(ptr), QtWidgets.QMainWindow)

def windowE():
    qMayaWindow = getMayaWindow()
    we = ErrorUI(qMayaWindow)
    we.show()
    return we