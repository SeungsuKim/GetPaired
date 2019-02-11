import random

import networkx as nx
import matplotlib.pyplot as plt

class Symester:

    def __init__(self):
        self.name = ""
        self.members = []
        self.graph = nx.Graph()
        self.groups = []

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

    def get_members(self):
        return self.members

    def draw_graph(self):
        nx.draw(self.graph, with_labels=True)
        plt.savefig("graph.png")

    def make_pairs(self, num_group):
        self._init_graph()

        seeds = random.sample(self.graph.nodes, num_group)
        for seed in seeds:
            self.graph.node[seed]['paired'] = True
            self.groups.append([seed])
        while len(self._unpaired_nodes()) >= num_group:
            for group in self.groups:
                unpaired_nodes = self._unpaired_nodes()
                if len(unpaired_nodes) == 0:
                    break
                optimal_node = ""
                min_distance = 999999999
                for node in unpaired_nodes:
                    distance = 0
                    for node_in_group in group:
                        distance += self.graph.get_edge_data(node, node_in_group)['distance']
                    if distance < min_distance:
                        optimal_node = node
                        min_distance = distance
                self.graph.node[optimal_node]['paired'] = True
                group.append(optimal_node)
        for node in self._unpaired_nodes():
            optimal_index = 0
            min_distance = 999999999
            for i, group in enumerate(self.groups):
                distance = 0
                for node_in_group in group:
                    distance += self.graph.get_edge_data(node, node_in_group)['distance']
                if distance < min_distance:
                    optimal_index = i
                    min_distance = distance
            self.graph.node[node]['paired'] = True
            self.groups[optimal_index].append(node)
        return self.groups

    def _init_graph(self):
        nx.set_node_attributes(self.graph, False, 'paired')
        nx.set_edge_attributes(self.graph, False, 'updated')
        self.groups = []

    def _unpaired_nodes(self):
        unpaired_nodes = []
        for node in self.graph.nodes(data='paired'):
            if not node[1]:
                unpaired_nodes.append(node[0])
        return unpaired_nodes

    def print_groups(self):
        for i, group in enumerate(self.groups):
            text = str(i+1)+". "
            for name in group:
                text += name
                text += " "
            print(text)

    def print_graph(self):
        for edge in self.graph.edges(data=True):
            print(edge)

    def update_graph(self):
        for group in self.groups:
            for node1 in group:
                for node2 in group:
                    if node1 != node2 and not self.graph.get_edge_data(node1, node2)['updated']:
                        self.graph[node1][node2]['updated'] = True
                        self.graph[node1][node2]['distance'] += 1

