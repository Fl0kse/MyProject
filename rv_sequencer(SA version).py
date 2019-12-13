# -*- coding: utf-8 -*-
import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPalette, QColor
from glob import glob
import re
from collections import OrderedDict
import subprocess
from threading import Thread
from PyQt5.QtCore import QProcess
import threading

nut_path = r'\\buka_srv\tools\mayaTools\Shelkunchik\scripts'
if nut_path not in sys.path:
    sys.path.append(nut_path)

rvSequencerUI = None

class RVSequencerUI(QtWidgets.QWidget):

    def __init__(self):
        super(RVSequencerUI,self).__init__()
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle(u'RV Movie Sequencer')
        self.setObjectName(u'RVSequencerMainWidget')

        # setStyleSheet
        self.setStyleSheet("background-color: rgb(77, 77, 77); color: white")

        #Main
        lay_main = QtWidgets.QVBoxLayout(self)
        self.setLayout(lay_main)

        # Setting class variables
        self.ep_list = []
        projects = (u'BUKA', u'Shelkunchik')
        phases = (u'layout', u'animation', u'dynamic', u'render', u'compose')

        # Building UI
        self.proj_line = TypeSelect(projects)
        self.phase_line = TypeSelect(phases)
        self.other_phase_box = AssetCheckBox(u'Include all Previous Steps in RV Sequence')
        self.main_but = AssetButton(u'Create RV Sequence')
        self.search = AssetSearch(label=u'Введите номер эпизода: ', inlabel=u'ep_')
        self.ln_error = QtWidgets.QLineEdit(text="", readOnly=True)

        #Add Widget
        # lay_main.addWidget(self.btn)
        lay_main.addWidget(self.proj_line)
        lay_main.addWidget(self.phase_line)
        lay_main.addWidget(self.other_phase_box)
        lay_main.addWidget(self.search)
        lay_main.addWidget(self.main_but)
        lay_main.addWidget(self.ln_error)

        # Setup UI
        self.other_phase_box.setChecked(True)
        self.phase_line.children()[-1].setChecked(True)
        self.proj_line.findChild(QtWidgets.QPushButton).setChecked(True)

        regex = QtCore.QRegExp(r"ep_[0-9][0-9][0-9][0-9]")
        validator = QtGui.QRegExpValidator(regex)
        self.search.line.setValidator(validator)

        # Connect Functions
        self.main_but.clicked.connect(self.generate_sequence)
        self.search.line.returnPressed.connect(self.generate_sequence)
        self.process = QProcess()

    def create_tree(self):
        print('')
        try:
            self.tree.clear()
            self.ep_list = []
            self.proj_line.setDisabled(True)
            self.phase_line.setDisabled(True)
            if self.proj_line.group.checkedId() < -1 and self.phase_line.group.checkedId() < -1:
                # activity = cerebro_defs.activity_by_name(self.phase_line.selectedText())
                project = self.proj_line.selectedText()
                phase = self.phase_line.selectedText()
                episode = self.search.line.text()
                # self.tasks_list = cerebro_defs.get_tasklist(activity, [self.proj_line.selectedText()], [16256013, 16256014])
                if self.ep_list:
                    self.tree.createTree(self.tasks_list)
                else:
                    empty_item = QtWidgets.QTreeWidgetItem(self.tree)
                    empty_item.setText(0, u'Ролики с такими параметрами не найдены')
        except Exception as err:
            cmds.warning(err)
        finally:
            self.proj_line.setDisabled(False)
            self.phase_line.setDisabled(False)

    def find_movies(self, project, phase, ep_pattern):
        default_dir = os.path.join(r"\\gamma", "" if project == "BUKA" else project, "03_Production")
        ep_sc_pattern = '{}_sc_[0-9][0-9][0-9][0-9]'.format(ep_pattern)
        patterns = {-2: r"{0}\{1}\{2}\layout\{2}.mov".format(default_dir, ep_pattern, ep_sc_pattern),
                    -3: r"{0}\{1}\{2}\animation\{2}.mov".format(default_dir, ep_pattern, ep_sc_pattern),
                    -4: r"{0}\{1}\{2}\clean_scene\{2}_occl.mov".format(default_dir, ep_pattern, ep_sc_pattern),
                    -5: r"{0}\{1}\{2}\renderoutput\{2}_render*.mov".format(default_dir, ep_pattern, ep_sc_pattern),
                    -6: r"\\bolero\{0}\04_Postproduction\{1}\mov\{2}_v[0-9][0-9][0-9].mov".format(project, ep_pattern, ep_sc_pattern)
                    }
        if not self.other_phase_box.isChecked():
            return glob(patterns[phase])
        all_shots = {os.path.splitext(os.path.basename(sh))[0]: "" for sh in glob(patterns[-2])}
        all_shots = OrderedDict(sorted(all_shots.items()))
        for i in range(phase, -1):
            founded = glob(patterns[i])
            for path in founded:
                sc_name = re.search(r"ep_\d{4}_sc_\d{4}", path).group()
                if sc_name in all_shots.keys() and not all_shots[sc_name]:
                    all_shots.update({sc_name: path})
            if all(scene for scene in all_shots.values()):
                return all_shots.values()
        return all_shots.values()

    def generate_sequence(self):
        project = self.proj_line.selectedText()
        phase = self.phase_line.group.checkedId()
        episode = self.search.line.text()
        mov_list = self.find_movies(project, phase, episode)
        if mov_list:
            self.merge_video(mov_list)
        else:
            print('No Movies Found')
            self.ln_error.setText('No Movies Found')

    def subprocess_thread(self, command):
        subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    #     subprocess.Popen(command).communicate()

    def execute_cmd(command, pool=None):
        cmd = command
        if not pool:
            pool = QtCore.QThreadPool().globalInstance()
        thread = CommandThread(cmd)
        pool.start(thread)
        return thread

    def merge_video(self, mov_list):
        rv_path = glob(r'C:\Program Files*\Shotgun\*\bin\rv.exe')
        if not rv_path:
            rv_path = glob(r'C:\Program Files*\Shotgun\*\bin\rvsdi.exe')
            if not rv_path:
                self.ln_error.setText(u'RV Player not Found')
                return
        # command = rv_path + list(mov_list)
        command = list(mov_list)
        process = QProcess(self)
        myProcess.start(program, arguments)
        # thred1 = Thread(target=self.subprocess_thread, args=(command))
        # thred1.start()
        # thred1.join()
        thread1 = subprocess_thread(command=command)
        thread1.start()
        thread1.join()
        # newcommand = ''
        # for el in command:
        #     newcommand += el
        # self.execute_cmd(command)
        # subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        # newcommand = ('subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()')
        # if self.process.isOpen():
        #     return
        # self.process.setProcessChannelMode(QProcess.SeparateChannels)
        # self.process.start(newcommand)
        # subprocess.run(command)
        # thread1 = subprocess_thread(command)
        # thread1.start()




class subprocess_thread(threading.Thread):

    def __init__(self, command):
        super().__init__(self, name="threddy" + command)
        self.command = command

    def run(self):
        subprocess.Popen(self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()




class TypeSelect(QtWidgets.QWidget):
    def __init__(self, names_set):
        styleSheetButton = u"""
            QPushButton {
                font:16px;
                height: 22px;
                background-color: #5b0000;
                border-radius: 5px;
                padding: 4px 6px 4px 6px;}
            QPushButton:closed {
                background-color: #5c5c5c;}
            QPushButton:pressed {
                background-color: #480000;
                border-style: inset;}"""
        super(TypeSelect, self).__init__()
        typelayout = QtWidgets.QHBoxLayout(self)
        typelayout.setContentsMargins(2, 0, 0, 2)
        typelayout.setSpacing(8)
        self.group = QtWidgets.QButtonGroup(self)
        for typ in names_set:
            but_item = QtWidgets.QPushButton(typ)
            but_item.setCheckable(True)
            but_item.setStyleSheet(styleSheetButton)
            self.group.addButton(but_item)
            typelayout.addWidget(but_item)

    def selectedText(self):
        return self.group.checkedButton().text()



class AssetSearch(QtWidgets.QWidget):
    def __init__(self, label=u'', inlabel=u''):
        super(AssetSearch, self).__init__()
        self.styleSheetLine = u"""
                    QLabel {
                    font:16px;
                    background-color: transparent;
                    }
                    QLineEdit {
                        background-color: rgb(51, 51, 51);
                        font:16px;
                        height: 28px;
                        padding: 1px;
                        border-radius: 5px;
                    }
                    QLineEdit[mode="Search"] {
                        padding-left: 30px;
                        qproperty-alignment: AlignLeft;
                    }
                    QLineEdit[mode="Bar"]{
                        padding-left: 6px;
                        qproperty-alignment: AlignCenter;
                    }"""
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        typelayout = QtWidgets.QHBoxLayout(self)
        if label:
            self.label = QtWidgets.QLabel(label)
            typelayout.addWidget(self.label)
        typelayout.setContentsMargins(0, 0, 0, 0)
        self.line = QtWidgets.QLineEdit(inlabel)
        self.line.setProperty('mode', 'Search')
        self.pix = QtWidgets.QLabel(self.line)
        self.pix.setPixmap(QtGui.QPixmap(r"\\buka_srv\tools\mayaTools\Shelkunchik\scripts\nut_assets\resources\icons\search.svg").scaled(25, 25))
        self.setStyleSheet(self.styleSheetLine)
        typelayout.addWidget(self.line)

    def switch_mode(self, mode):
        self.line.setProperty('mode', mode)
        if mode == 'Search':
            self.pix.setHidden(False)
            self.line.setReadOnly(False)
            self.line.setEnabled(True)
            self.line.setStyleSheet(self.styleSheetLine)
        elif mode == 'Bar':
            self.pix.setHidden(True)
            self.line.setReadOnly(True)
            self.line.setEnabled(False)
            self.line.setStyleSheet(self.styleSheetLine)



class AssetButton(QtWidgets.QPushButton):
    def __init__(self, text=u'Выложить'):
        styleSheetButton = u"""
            QPushButton {
                font:16px;
                height: 22px;
                background-color: #373737;
                border-radius: 5px;
                padding: 4px 6px 4px 6px;
                }
            QPushButton:pressed {
                background-color: #480000;}"""
        super(AssetButton, self).__init__()
        self.setStyleSheet(styleSheetButton)
        self.setText(text)



class AssetCheckBox(QtWidgets.QCheckBox):
    def __init__(self, parent=None):
        super(AssetCheckBox, self).__init__(parent)
        styleSheetCheckBox = u"""
            QCheckBox {
                font:15px;
                height: 22px;
                padding-bottom: 4px;
            }
            QCheckBox:indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox:indicator:checked {
                image: url(//buka_srv/tools/mayaTools/Shelkunchik/scripts/nut_assets/resources/icons/checkbox_checked.svg);
            }
            QCheckBox:indicator:pressed {
                image: url(//buka_srv/tools/mayaTools/Shelkunchik/scripts/nut_assets/resources/icons/checkbox_pressed.svg);
            }
        """
        self.setStyleSheet(styleSheetCheckBox)



class CommandThread(QtCore.QRunnable):
    def __init__(self, cmd, parent=None):
        super(CommandThread, self).__init__(parent)
        self.cmd = cmd
        self.signal = ThreadSignal()

    def run(self):
        # _no_window = subprocess.STARTUPINFO()
        # _no_window.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        res = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        self.signal.obj.emit(res)
        return res




class ThreadSignal(QtCore.QObject):
    # obj = QtCore.Signal(object)
    obj = QtCore.pyqtSignal(object)
    # status = QtCore.Signal(object)
    status = QtCore.pyqtSignal(object)
    # progress = QtCore.Signal(int)
    progress = QtCore.pyqtSignal(int)
    # finished = QtCore.Signal()
    finished = QtCore.pyqtSignal()




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    w = RVSequencerUI()
    w.show()
    sys.exit(app.exec_())