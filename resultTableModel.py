from PyQt5.QtCore import QAbstractTableModel


class ResultTableModel(QAbstractTableModel):

    def __init__(self, parent, groups, *args):
        QAbstractTableModel.__init__(self, parent, *args)

        self.groups = groups

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
        try:
            return self.groups[index.column()][index.row()]
        except IndexError:
            return ""
