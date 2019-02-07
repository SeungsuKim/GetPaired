from symester import Symester

class GetPaired:

    def __init__(self):
        self.symesters = []
        self.cur_symester = None

    def add_symester(self, symester):
        self.symesters.append(symester)

    def is_symester_exists(self):
        return len(self.symesters) != 0

    def num_symesters(self):
        return len(self.symesters)

    def print_symesters(self):
        text = ""
        for i, symester in enumerate(self.symesters):
            text += "%d. %s   " % (i+1, symester.get_name())
        print(text)

    def set_cur_symester(self, index):
        self.cur_symester = self.symesters[index]

    def print_members(self):
        print(self.cur_symester.members)


