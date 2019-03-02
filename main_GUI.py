import os
import sys
import pickle
from copy import deepcopy

from get_paired import GetPaired
from tableModel import MemberTableModel, ResultTableModel
from PyQt5.QtWidgets \
    import QApplication, QWidget, QMainWindow, QLabel, \
    QComboBox, QHBoxLayout, QVBoxLayout, QGridLayout, \
    QPushButton, QTableWidget, QTableWidgetItem, QSpinBox, \
    QTableView
from PyQt5 import QtCore, QtWidgets


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
        lb_group = QLabel('그룹 수 입력')
        self.sb_group = QSpinBox()
        self.sb_group.setMinimum(2)
        self.sb_group.setMaximum(self.get_paired.cur_symester.get_num_members())
        btn_done = QPushButton('완료')
        btn_done.clicked.connect(self.resultWindow)

        vbox_group = QVBoxLayout()
        vbox_group.addStretch(1)
        vbox_group.addWidget(lb_group)
        vbox_group.addWidget(self.sb_group)
        vbox_group.addStretch(1)
        vbox_group.addWidget(btn_done)
        vbox_group.addStretch(1)

        members = deepcopy(self.get_paired.cur_symester.get_members())
        self.memberTableModel = MemberTableModel(self, members)
        self.memberTable = QTableView()
        self.memberTable.setModel(self.memberTableModel)
        self.memberTable.clicked.connect(self.memberTableModel.itemClicked)
        self.memberTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        btn_remove = QPushButton('삭제')
        btn_remove.clicked.connect(self.memberTableModel.removeCheckedMembers)
        btn_reset = QPushButton('초기화')
        btn_reset.clicked.connect(lambda: self.memberTableModel.resetMembers(deepcopy(self.get_paired.cur_symester.get_members())))

        hbox_btn_remove = QHBoxLayout()
        hbox_btn_remove.addStretch(1)
        hbox_btn_remove.addWidget(btn_remove)
        hbox_btn_remove.addWidget(btn_reset)

        vbox_table = QVBoxLayout()
        vbox_table.addWidget(self.memberTable)
        vbox_table.addLayout(hbox_btn_remove)

        hbox_main = QHBoxLayout()
        hbox_main.addStretch(1)
        hbox_main.addLayout(vbox_table)
        hbox_main.addStretch(1)
        hbox_main.addLayout(vbox_group)
        hbox_main.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addWidget(lb_cur_symester)
        vbox.addLayout(hbox_main)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 600, 400)
        self.show()

    def resultWindow(self):
        self.close()
        self.get_paired.active_members = self.memberTableModel.members
        self.next = ResultWindow(self.get_paired, self.sb_group.value())


class ResultWindow(QWidget):

    def __init__(self, get_paired, num_group):
        super().__init__()

        self.get_paired = get_paired
        self.num_group = num_group

        self.initUI()

    def initUI(self):
        btn_apply = QPushButton('적용')
        btn_retry = QPushButton('재시도')
        btn_retry.clicked.connect(self.retry)
        btn_back = QPushButton('뒤로')
        btn_back.clicked.connect(self.mainWindow)

        hbox_btn = QHBoxLayout()
        hbox_btn.addWidget(btn_back)
        hbox_btn.addStretch(1)
        hbox_btn.addWidget(btn_apply)
        hbox_btn.addWidget(btn_retry)

        groups = self.get_paired.cur_symester.make_pairs(self.num_group)
        self.resultTableModel = ResultTableModel(self, groups)
        self.resultTable = QTableView()
        self.resultTable.setModel(self.resultTableModel)
        self.resultTable.clicked.connect(self.resultTableModel.itemClicked)
        self.resultTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        vbox = QVBoxLayout()
        vbox.addWidget(self.resultTable)
        vbox.addLayout(hbox_btn)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 600, 400)
        self.show()

    def retry(self):
        groups = self.get_paired.cur_symester.make_pairs(self.num_group)
        self.resultTableModel.setGroups(groups)

    def mainWindow(self):
        self.close()
        self.next = MainWindow(self.get_paired)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InitialWindow()
    sys.exit(app.exec_())
