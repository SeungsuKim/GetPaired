from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import Qt


class MemberTableModel(QAbstractTableModel):

    def __init__(self, parent, members):
        QAbstractTableModel.__init__(self, parent)

        self.members = members
        self.isChecked = [False] * len(self.members)
        self.checkedMembers = []

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

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return ["참여 인원"][section]
            if orientation == Qt.Vertical:
                return str(section+1)

    def itemClicked(self, item):
        self.layoutAboutToBeChanged.emit()

        if self.isChecked[item.row()]:
            self.isChecked[item.row()] = False
            self.checkedMembers.remove(str(item.data()))
        else:
            self.isChecked[item.row()] = True
            self.checkedMembers.append(str(item.data()))

        self.layoutChanged.emit()

    def addMember(self, member):
        self.layoutAboutToBeChanged.emit()
        self.members.append(member)
        self.isChecked.append(False)
        self.layoutChanged.emit()

    def uncheckEveryMember(self):
        self.layoutAboutToBeChanged.emit()
        self.isChecked = [False] * len(self.members)
        self.checkedMembers = []
        self.layoutChanged.emit()

    def removeCheckedMembers(self):
        self.layoutAboutToBeChanged.emit()
        for member in self.checkedMembers:
            self.members.remove(member)
        self.isChecked = [False] * len(self.members)
        self.checkedMembers = []
        self.layoutChanged.emit()

    def resetMembers(self, members):
        self.layoutAboutToBeChanged.emit()

        self.members = members
        self.isChecked = [False] * len(self.members)
        self.checkedMembers = []

        self.layoutChanged.emit()


class AntiMemberTableModel(QAbstractTableModel):

    def __init__(self, parent):
        QAbstractTableModel.__init__(self, parent)

        self.antiMembers = []
        self.isChecked = []

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.antiMembers)

    def columnCount(self, parent=None, *args, **kwargs):
        return 3

    def data(self, index, role=None):
        if not index.isValid():
            return None
        if index.column() == 0:
            if role == Qt.CheckStateRole:
                if self.isChecked[index.row()]:
                    return Qt.Checked
                else:
                    return Qt.Unchecked
        else:
            if role == Qt.DisplayRole or role == Qt.EditRole:
                return self.antiMembers[index.row()][index.column()-1]
            elif role == Qt.TextAlignmentRole:
                return Qt.AlignCenter

    def headerData(self, section, orientation, role=None):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return ['선택', '인원1', '인원2'][section]
            if orientation == Qt.Vertical:
                return str(section+1)

    def addAntiMember(self, members):
        if self._isMemberAlreadyExist(members):
            return False
        self.layoutAboutToBeChanged.emit()
        self.antiMembers.append(members)
        self.isChecked.append(False)
        self.layoutChanged.emit()
        return True

    def _isMemberAlreadyExist(self, members):
        for antiMember in self.antiMembers:
            if members[0] in antiMember:
                anotherAntiMember = antiMember[(antiMember.index(members[0])+1)%2]
                if anotherAntiMember == members[1]:
                    return True
        return False

    def removeAntiMember(self):
        self.layoutAboutToBeChanged.emit()
        for i, checked in reversed(list(enumerate(self.isChecked))):
            if checked:
                self.antiMembers.pop(i)
        self.isChecked = [False] * len(self.antiMembers)
        self.layoutChanged.emit()

    def itemClicked(self, item):
        if item.column() == 0:
            self.layoutAboutToBeChanged.emit()
            self.isChecked[item.row()] = not self.isChecked[item.row()]
            self.layoutChanged.emit()


class ResultTableModel(QAbstractTableModel):

    def __init__(self, parent, groups):
        QAbstractTableModel.__init__(self, parent)

        self.groups = groups
        self.col = max([len(group) for group in self.groups])
        self.row = len(self.groups)
        self.isChecked = [[False]*self.col for _ in range(self.row)]
        self.checkedItems = []

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
        if self.isChecked[item.column()][item.row()]:
            self.isChecked[item.column()][item.row()] = False
            self.checkedItems.remove(item)
        else:
            self.isChecked[item.column()][item.row()] = True
            self.checkedItems.append(item)
        self.layoutChanged.emit()

    def exchangeCheckedMembers(self):
        if len(self.checkedItems) != 2:
            return False
        if self._isCheckedMembersInTheSameGroup():
            return False
        self.layoutAboutToBeChanged.emit()
        if not '' in [str(item.data()) for item in self.checkedItems]:
            self.groups[self.checkedItems[0].column()][self.checkedItems[0].row()], \
            self.groups[self.checkedItems[1].column()][self.checkedItems[1].row()] = \
            self.groups[self.checkedItems[1].column()][self.checkedItems[1].row()], \
            self.groups[self.checkedItems[0].column()][self.checkedItems[0].row()]
        else:
            emptyIndex = [str(item.data()) for item in self.checkedItems].index('')
            emptyItem = self.checkedItems[emptyIndex]
            memberItem = self.checkedItems[(emptyIndex+1)%2]
            self.groups[emptyItem.column()].append(self.groups[memberItem.column()].pop(memberItem.row()))
        self.isChecked = [[False] * self.col for _ in range(self.row)]
        self.checkedItems = []
        self.layoutChanged.emit()
        return True

    def _isCheckedMembersInTheSameGroup(self):
        return self.checkedItems[0].column()\
               == self.checkedItems[1].column()


