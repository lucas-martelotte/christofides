from typing import List, Tuple


class EulerCycle():
    def __init__(self, edges: List[Tuple[int, int]]):
        self.number_of_vertices = 0
        self.edges = [e for e in edges]

    def euler_cycle(self):
        edges = [e for e in self.edges]
        root = self.edges[0][0]
        path: List[int] = []
        path = self.__dfs(root, edges, path)
        return path

    def __dfs(self, u, edges, path):
        u_edges = self.find_edges(u, edges)
        while u_edges != []:
            edge_to_follow = u_edges.pop()
            edges.remove(edge_to_follow)
            next_vertice = edge_to_follow[0] if edge_to_follow[1] == u else edge_to_follow[1]
            path = self.__dfs(next_vertice, edges, path)
            u_edges = self.find_edges(u, edges)
        path.insert(0, u)
        return path

    def find_edges(self, u: int, edges: List[Tuple[int, int]]):
        return [e for e in edges if (u in [e[0], e[1]])]
