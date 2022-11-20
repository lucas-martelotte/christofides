from typing import List, Tuple, Set

from kruskal import Kruskal
from graph import WeightedGraph


class LowerBound1Tree():
    def __init__(self, graph: WeightedGraph):
        self.graph = graph

    def get_maximum_1_tree(self) -> Tuple[Set[Tuple[int, int]], float]:
        max_cost = 0
        max_tree = set()
        for v in self.graph.vertices():
            graph_without_v_edges = self.graph.remove_edges(
                set([e for e in self.graph.edges() if v in list(e)])
            )
            v_mst = Kruskal(graph_without_v_edges).minimum_spanning_tree()
            v_mst_without_duplicates: Set[Tuple[int, int]] = set()
            for e in v_mst:
                if (e[1], e[0]) not in v_mst_without_duplicates:
                    v_mst_without_duplicates.add(e)
            one_tree = v_mst_without_duplicates.union(
                self.__two_cheapest_edges(v)
            )
            cost = self.graph.cost(one_tree)
            if cost > max_cost:
                max_cost = cost
                max_tree = one_tree
        return max_tree, max_cost

    def __two_cheapest_edges(self, v: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """
            Returns the two edges from v that have the lowest cost. If v
            does not belong in the graph, or v has less than two edges,
            raises an Exception.
        """
        v_edges = [e for e in self.graph.edges() if e[0] == v]
        v_edges.sort(key=(lambda e: self.graph.cost_dict[e]))
        return (v_edges[0], v_edges[1])
