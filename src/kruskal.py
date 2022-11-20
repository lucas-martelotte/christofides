from typing import List, Tuple, Set

from graph import WeightedGraph
from union_find import UnionFind


class Kruskal():
    def __init__(self, graph: WeightedGraph):
        self.graph = graph

    def minimum_spanning_tree(self) -> Set[Tuple[int, int]]:
        tree: Set[Tuple[int, int]] = set()
        uf = UnionFind(self.graph.number_of_vertices)
        sorted_edges = [e for e in self.graph.edges()]
        sorted_edges.sort(key=(lambda e: self.graph.cost_dict[e]))
        for v, w in sorted_edges:
            if uf.find(v) != uf.find(w):
                tree = tree.union({(v, w), (w, v)})
                uf.union(v, w)
        return tree
