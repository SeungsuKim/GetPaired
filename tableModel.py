from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import Qt


class MemberTableModel(QAbstractTableModel):

    def __init__(self, parent, members):
        QAbstractTableModel.__init__(self, parent)

        self.members = members
        self.isChecked = [False] * len(self.members)
        self.checkedItems = []

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.members)

    def columnCount(self, parent=None, *args, **kwargs):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return self.members[index.row()]
        elif role == Qt.CheckStateRole:
            if self.isChecked[index.row()]:
                return Qt.Checked
            else:
                return Qt.Unchecked
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

    def itemClicked(self, item):
        self.layoutAboutToBeChanged.emit()

        if self.isChecked[item.row()]:
            self.isChecked[item.row()] = False
            self.checkedItems.remove(item)
        else:
            self.isChecked[item.row()] = True
            self.checkedItems.append(item)

        self.layoutChanged.emit()

    def removeCheckedMembers(self):
        self.layoutAboutToBeChanged.emit()

        for item in self.checkedItems:
            self.members.remove(str(item.data()))
        self.isChecked = [False] * len(self.members)
        self.checkedItems = []

        self.layoutChanged.emit()

    def resetMembers(self, members):
        self.layoutAboutToBeChanged.emit()

        self.members = members
        self.isChecked = [False] * len(self.members)
        self.checkedItems = []

        self.layoutChanged.emit()


class ResultTableModel(QAbstractTableModel):

    def __init__(self, parent, groups):
        QAbstractTableModel.__init__(self, parent)

        self.groups = groups
        col = max([len(group) for group in self.groups])
        row = len(self.groups)
        self.isChecked = [[False]*col for _ in range(row)]

    def setGroups(self, groups):
        self.layoutAboutToBeChanged.emit()
        self.groups = groups
        self.layoutChanged.emit()

    def rowCount(self, parent=None, *args, **kwargs):
        return max([len(group) for group in self.groups])

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.groups)

    def data(self, index, role):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole or role == Qt.EditRole:
            try:
                return self.groups[index.column()][index.row()]
            except IndexError:
                return ""
        elif role == Qt.CheckStateRole:
            if self.isChecked[index.column()][index.row()]:
                return Qt.Checked
            else:
                return Qt.Unchecked
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

    def itemClicked(self, item):
        self.layoutAboutToBeChanged.emit()
        self.isChecked[item.column()][item.row()] = \
            not self.isChecked[item.column()][item.row()]
        self.layoutChanged.emit()
