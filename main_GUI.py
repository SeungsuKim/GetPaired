import os
import sys
import pickle

from get_paired import GetPaired
from symester import Symester
from PyQt5.QtWidgets \
    import QApplication, QWidget, QMainWindow, QLabel, \
    QComboBox, QHBoxLayout, QVBoxLayout, QGridLayout, \
    QPushButton, QTableWidget, QTableWidgetItem


class InitialWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.loadData()
        self.initUI()

    def loadData(self):
        # If data file does not exists, make new data file.
        if not os.path.exists("data.pkl"):
            with open('data.pkl', 'wb') as f:
                self.get_paired = GetPaired()
                pickle.dump(self.get_paired, f)

        # Load GetPaired instance from the data file.
        with open('data.pkl', 'rb') as f:
            self.get_paired = pickle.load(f)

    def initUI(self):
        lb_new_symester = QLabel('새 학기 시작')
        btn_new_symeser = QPushButton('새 학기')

        lb_symester = QLabel('기존 학기 선택')
        cb_symester = QComboBox(self)
        cb_symester.clear()
        cb_symester.addItems(self.get_paired.get_symester_names())
        cb_symester.activated.connect(self.mainWindow)

        grid_symester = QGridLayout()
        grid_symester.addWidget(lb_new_symester, 0, 0)
        grid_symester.addWidget(btn_new_symeser, 1, 0)
        grid_symester.addWidget(lb_symester, 0, 1)
        grid_symester.addWidget(cb_symester, 1, 1)

        btn_setting = QPushButton('설정')

        hbox_setting = QHBoxLayout()
        hbox_setting.addStretch(1)
        hbox_setting.addWidget(btn_setting)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(grid_symester)
        vbox.addStretch(1)
        vbox.addLayout(hbox_setting)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 150)
        self.show()

    def mainWindow(self, index):
        self.get_paired.set_cur_symester(index)
        self.close()
        self.next = MainWindow(self.get_paired)

class MainWindow(QWidget):

    def __init__(self, get_paired):
        super().__init__()

        self.get_paired = get_paired

        self.initUI()

    def initUI(self):
        lb_cur_symester = QLabel(self.get_paired.cur_symester.get_name())

        self.createMemberTable()

        hbox_main = QHBoxLayout()
        hbox_main.addWidget(self.memberTable)
        hbox_main.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addWidget(lb_cur_symester)
        vbox.addLayout(hbox_main)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 600, 400)
        self.show()

    def createMemberTable(self):
        self.memberTable = QTableWidget()
        self.memberTable.setColumnCount(1)
        members = self.get_paired.cur_symester.get_members()
        self.memberTable.setRowCount(len(members))
        for i, member in enumerate(members):
            item = QTableWidgetItem(member)
            self.memberTable.setItem(i, 0, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InitialWindow()
    sys.exit(app.exec_())
