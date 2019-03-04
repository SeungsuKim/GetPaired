class GetPaired:

    def __init__(self):
        self.symesters = []
        self.cur_symester = None

    def add_symester(self, symester):
        self.symesters.append(symester)

    def get_symester_names(self):
        def name(symester):
            return symester.get_name()
        return list(map(name, self.symesters))

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

    def remove_symester(self, index):
        print(self.symesters)
        self.symesters.pop(index)
        print(self.symesters)

    def reset_symester(self, index):
        self.symesters[index].reset()

    def print_members(self):
        print(self.cur_symester.members)


