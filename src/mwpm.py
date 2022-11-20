from typing import List, Tuple
import networkx as nx  # type: ignore

from graph import WeightedGraph


class MinimumWeightPerfectMatching():
    def __init__(self, graph: WeightedGraph):
        self.graph = graph

    def minimum_weight_perfect_matching(self) -> List[Tuple[int, int]]:
        nx_graph = nx.Graph()
        max_weight = max([w for w in self.graph.cost_dict.values()])
        for v, w in self.graph.edges():
            nx_graph.add_edge(str(v), str(w),
                              weight=max_weight+1-self.graph.cost_dict[(v, w)])
        pm = nx.max_weight_matching(nx_graph, weight="weight")
        return [(int(v), int(w)) for v, w in pm]
