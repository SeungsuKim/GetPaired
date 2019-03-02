from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import Qt


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
