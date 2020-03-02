from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import subprocess
import os
from base64 import b64decode as b64d

class MainUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainUI, self).__init__()
        self.setWindowTitle("111")
        self.wdg_main = QtWidgets.QWidget(self)
        self.setCentralWidget(self.wdg_main)
        self.lay = QtWidgets.QHBoxLayout()
        self.wdg_main.setLayout(self.lay)
        self.ln = QtWidgets.QLineEdit()
        self.btn = QtWidgets.QPushButton('Do')
        self.lay.addWidget(self.ln)
        self.lay.addWidget(self.btn)
        self.btn.clicked.connect(self.epta_logika)
        self.ln.returnPressed.connect(self.btn.click)

    def epta_logika(self):
        path = self.ln.text()
        pathlist = path.split('\\')
        pathlist.pop(0)
        pathlist.pop(0)
        keyword = pathlist[0].lower()
        pathlist.pop(0)
        if keyword == 'delta':
            newPath = r'E:\02_Preproduction'
            PS_FILE = r"\\BUKA_SRV\tools\mayaTools\site-packages\PSTools\psfile.exe"
            for letter in pathlist:
                newPath += '\\' + letter
            # commandStr = PS_FILE + ' \\\\' + keyword + ' ' + '"' + newPath + '"' + ' -c'
            print('111')
            commandStr = '{} -u {} -p {} \\\\{} "{}" -c'.format(PS_FILE, b64d(_user), b64d(_pwd), keyword, newPath)
            print(commandStr)
            # execute_cmd(commandStr)
            print('222')
            os.system(commandStr)
            print('Ok')

# def execute_cmd(command):
#     from base64 import b64decode as b64d
#
#     _cpau_binary = r'\\buka_srv\tools\mayaTools\site-packages\cpau'
#     _user = '***'
#     _pwd = '***'
#     cmd = [_cpau_binary, '-u', b64d(_user), '-p', b64d(_pwd), '-ex', command, '-nowarn', '-c', '-hide', '-wait', '-outprocexit']  #'-hide', '-wait', '-outprocexit']
#
#     # print(cmd)
#     # sep = ' '
#     # newcmd = sep.join(cmd)
#     # print(newcmd)
#     # return subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
#     #                         startupinfo=_no_window).communicate()[0]
#     # print(subprocess.run(cmd))




if __name__ == '__main__':
    app =  QtWidgets.QApplication(sys.argv)
    w = MainUI()
    w.show()
    sys.exit(app.exec_())
