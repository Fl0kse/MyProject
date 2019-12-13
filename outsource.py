from PyQt5 import QtCore, QtWidgets, QtGui
import sys




class MainUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainUI, self).__init__()
        self.setWindowTitle('Outsource')
        self.setWindowFlags(QtCore.Qt.Window)
        self.setMinimumSize(800, 500)

        # setStyleSheet
        self.setStyleSheet("background-color: rgb(77, 77, 77); color: white")

        # Tab Widget
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)




class MyTableWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(QtWidgets.QWidget, self).__init__(parent)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.count = 0

        # Add Tree
        self.export_tree = ScenesTree(['Scenes', 'Mode'])
        self.import_tree = ScenesTree(['Scenes', 'Mode'])
        self.referens_tree = ScenesTree(['Outsource References Found', 'Studio Deferences Match'])

        # Initialize tab screen
        self.tabs = QtWidgets.QTabWidget()
        self.tab_export = QtWidgets.QWidget()
        self.tab_import = QtWidgets.QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab_export, "Export to outsourcing")
        self.tabs.addTab(self.tab_import, "Import from outsorcing")

        # Icon
        self.icon_folder = QtGui.QIcon()
        self.icon_folder.addPixmap(QtGui.QPixmap(r"D:\Artyom\Prog\Python\outsource\src\folder.ico"))
        self.icon_arrow_down = QtGui.QIcon()
        self.icon_arrow_down.addPixmap(QtGui.QPixmap(r"D:\Artyom\Prog\Python\outsource\src\arrow-down-sign-to-navigate.png"))

        ############ Create first tab
        self.tab_export.layout = QtWidgets.QVBoxLayout(self)
        self.tab_export.setLayout(self.tab_export.layout)

        # Widget Export Project Properties
        self.wdg_epp = QtWidgets.QWidget()
        self.lay_epp = QtWidgets.QVBoxLayout()
        self.wdg_epp.setLayout(self.lay_epp)
        self.wdg_epp_fr = QtWidgets.QWidget()
        self.lay_epp_fr = QtWidgets.QHBoxLayout()
        self.wdg_epp_fr.setLayout(self.lay_epp_fr)
        self.lay_epp.addWidget(self.wdg_epp_fr)

        self.lab_epp = QtWidgets.QLabel('Project folder: ')
        self.ln_epp = QtWidgets.QLineEdit()
        self.btn_epp = QtWidgets.QPushButton('set Project folder')
        self.btn_epp.setIcon(self.icon_folder)
        self.ln_epp_error = QtWidgets.QLineEdit(text="Project is not found. Set Project first", readOnly=True)
        self.ln_epp_error.setStyleSheet("background-color: #FF6400")

        self.lay_epp_fr.addWidget(self.lab_epp)
        self.lay_epp_fr.addWidget(self.ln_epp)
        self.lay_epp_fr.addWidget(self.btn_epp)
        self.lay_epp.addWidget(self.ln_epp_error)

        # Widget Export Current Scene
        self.wdg_ecs = QtWidgets.QWidget()
        self.lay_ecs = QtWidgets.QHBoxLayout()
        self.wdg_ecs.setLayout(self.lay_ecs)

        self.lab_ecs = QtWidgets.QLabel('Scene name: ')
        self.ln_ecs = QtWidgets.QLineEdit()
        self.btn_ecs = QtWidgets.QPushButton('Add to Project')
        self.btn_ecs.setIcon(self.icon_folder)


        self.lay_ecs.addWidget(self.lab_ecs)
        self.lay_ecs.addWidget(self.ln_ecs)
        self.lay_ecs.addWidget(self.btn_ecs)

        # Widget Export Multiple Scenes
        self.wdg_ems = QtWidgets.QWidget()
        self.lay_ems = QtWidgets.QHBoxLayout()
        self.wdg_ems.setLayout(self.lay_ems)

        # self.lab_ems = QtWidgets.QLabel('Drag and Drop or Paste scenes to the tree. When all scenes dropped press the Button for convert')
        self.btn_ems = QtWidgets.QPushButton('Add all queued scenes to the Project')
        self.btn_ems.setIcon(self.icon_folder)

        # self.lay_ems.addWidget(self.lab_ems)
        self.lay_ems.addWidget(self.btn_ems)

        # Add Widgets to ToolBox
        # self.tool_export = QtWidgets.QToolBox()
        # self.tool_export.addItem(self.wdg_epp, 'Export Project Properties')
        # self.tool_export.addItem(self.wdg_ecs, 'Export Current Scene')
        # self.tool_export.addItem(self.wdg_ems, 'Export Multiple Scenes')

        # Add insert Button
        self.btn_inser = QtWidgets.QPushButton('Export Current Scene')
        self.btn_inser.setIcon(self.icon_arrow_down)

        # Add widget to TabWidget
        self.tab_export.layout.addWidget(self.wdg_epp)
        self.tab_export.layout.addWidget(self.btn_inser)
        self.tab_export.layout.addWidget(self.export_tree)
        self.tab_export.layout.addWidget(self.wdg_ems)

        # Button connect
        self.btn_inser.clicked.connect(self.insertWidget)
        ############

        ############ Create second tab
        self.tab_import.layout = QtWidgets.QVBoxLayout(self)
        self.tab_import.setLayout(self.tab_import.layout)

        # Central layout
        self.wdg_ifo = QtWidgets.QWidget()
        self.lay_ifo = QtWidgets.QHBoxLayout()
        self.wdg_ifo.setLayout(self.lay_ifo)

        # Central widget
        self.lab_ifo = QtWidgets.QLabel('Drag and Drop or Paste scenes to the tree. If any reference match is incirrect, choose it and Press Button')
        self.btn_ifo = QtWidgets.QPushButton('Replace Reference')
        self.btn_ifo.setIcon(self.icon_folder)

        # Add Widgets to main Widget
        self.lay_ifo.addWidget(self.lab_ifo)
        self.lay_ifo.addWidget(self.btn_ifo)

        self.tab_import.layout.addWidget(self.referens_tree)
        self.tab_import.layout.addWidget(self.wdg_ifo)
        self.tab_import.layout.addWidget(self.import_tree)
        ############

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def insertWidget(self):
        self.count += 1
        if self.count % 2 != 0:
            self.tab_export.layout.insertWidget(2, self.wdg_ecs)
        else:
            self.wdg_ecs.setParent(None)

    def Widget_ECS(self):
        self.wdg_ecs = QtWidgets.QWidget()
        self.lay_ecs = QtWidgets.QHBoxLayout()
        self.wdg_ecs.setLayout(self.lay_ecs)

        self.lab_ecs = QtWidgets.QLabel('Scene name: ')
        self.ln_ecs = QtWidgets.QLineEdit()
        self.btn_ecs = QtWidgets.QPushButton('Add to Project')
        self.btn_ecs.setIcon(self.icon_folder)


        self.lay_ecs.addWidget(self.lab_ecs)
        self.lay_ecs.addWidget(self.ln_ecs)
        self.lay_ecs.addWidget(self.btn_ecs)
        return self.wdg_ecs

    def add_multiple_scenes(self):
        queued_scenes = {}
        parent = self.tree.invisibleRootItem()
        for i in range(parent.childCount()):
            scene = parent.child(i)
            scene_name = scene.text(0)
            net_path = scene.text(2)
            mode = scene.text(1)
            if mode == 'Queued':
                queued_scenes[scene_name] = net_path
        for name, path in queued_scenes.items():
            self.add_to_project(name, current=False, net_path=path)





class ScenesTree(QtWidgets.QTreeWidget):

    def __init__(self, HeaderList, parent=None):
        super(ScenesTree, self).__init__(parent)
        self.setColumnCount(2)
        self.setColumnWidth(0, 250)
        self.setColumnWidth(1, 50)
        self.setHeaderLabels(HeaderList)




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    w = MainUI()
    w.show()
    sys.exit(app.exec_())