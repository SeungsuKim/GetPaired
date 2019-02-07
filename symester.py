import networkx as nx
import matplotlib.pyplot as plt

class Symester:

    def __init__(self):
        self.name = ""
        self.members = []
        self.graph = nx.Graph()

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_members(self, members):
        self.members = members
        self.graph.add_nodes_from(members)
        for node1 in self.graph.nodes:
            for node2 in self.graph.nodes:
                if node1 != node2:
                    self.graph.add_edge(node1, node2, distance=0)

    def add_member(self, member):
        if type(member) != str:
            raise TypeError("Member must be a string.")
        self.members.append(member)

    def add_members(self, members):
        if type(members) != list:
            raise TypeError("Members must be a list of string.")
        for member in members:
            if type(member) != str:
                raise TypeError("Members must be a list of string.")
        self.members += members

    def draw_graph(self):
        nx.draw(self.graph, with_labels=True)
        plt.savefig("graph.png")


