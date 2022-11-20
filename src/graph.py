from typing import List, Dict, Tuple, Set
import math
import random
import pygame


class Graph():
    def __init__(
        self,
        number_of_vertices: int,
        adj_matrix: List[List[bool]]
    ):
        self.number_of_vertices = number_of_vertices
        self.adj_matrix = adj_matrix
        if len(self.adj_matrix) != self.number_of_vertices:
            print(f"ERROR: Wrong adjacency matrix size. Expected {self.number_of_vertices}. " +
                  f"Got {len(self.adj_matrix)}.")
            raise Exception
        for v in self.vertices():
            if len(self.adj_matrix[v]) != self.number_of_vertices:
                print(f"ERROR: Wrong adjacency matrix size at vertice {v}. " +
                      f"Expected {self.number_of_vertices}. " +
                      f"Got {len(self.adj_matrix[v])}.")
                raise Exception
        for v in self.vertices():
            for w in self.vertices():
                if adj_matrix[v][w] != adj_matrix[w][v]:
                    print("ERROR: graph must be undirected!")
                    raise Exception

    def induced_graph(self, vertices: List[int]):
        """
            Returns the graph induced by the input vertices.
        """
        if max(vertices) >= self.number_of_vertices:
            print("ERROR: Input vertices must be in the graph!")
            raise Exception
        induced_number_of_vertices = len(vertices)
        induced_adj_matrix = [[False for _ in range(induced_number_of_vertices)]
                              for _ in range(induced_number_of_vertices)]
        for i in range(induced_number_of_vertices):
            for j in range(induced_number_of_vertices):
                v, w = vertices[i], vertices[j]
                if self.adj_matrix[v][w]:
                    induced_adj_matrix[i][j] = True
        return Graph(induced_number_of_vertices, induced_adj_matrix)

    def remove_vertice(self, vertice: int):
        """
            Returns a new graph without the input vertice.
        """
        if vertice not in self.vertices():
            return Graph(self.number_of_vertices, self.adj_matrix)
        number_of_vertices = self.number_of_vertices - 1
        adj_matrix = [[self.adj_matrix[v][w]
                       for v in self.vertices() if v != vertice]
                      for w in self.vertices() if w != vertice]
        for v in range(len(self.vertices())-1):
            if len(adj_matrix[v]) != len(self.vertices())-1:
                print(f"ERROR: Resulting matrix after " +
                      f"removing vertice {vertice} is wrong.")
                raise Exception
        return Graph(number_of_vertices, adj_matrix)

    def edges(self) -> List[Tuple[int, int]]:
        return [(v, w) for v in self.vertices() for w in self.vertices() if self.adj_matrix[v][w]]

    def vertices(self) -> List[int]:
        return [i for i in range(self.number_of_vertices)]

    def __str__(self) -> str:
        return f"Vertices:\t{self.vertices()}\n" +\
               f"Edges:\t{self.edges()}"


class WeightedGraph(Graph):
    def __init__(
        self,
        number_of_vertices: int,
        adj_matrix: List[List[bool]],
        cost_dict: Dict[Tuple[int, int], float]
    ):
        super().__init__(number_of_vertices, adj_matrix)
        self.cost_dict = cost_dict
        for v in self.vertices():
            for w in self.vertices():
                if not self.adj_matrix[v][w]:
                    continue
                if self.cost_dict.get((v, w)) is None or cost_dict.get((w, v)) is None:
                    print("ERROR: Cost must be defined for all edges!")
                    raise Exception
                if self.cost_dict.get((v, w)) != cost_dict.get((w, v)):
                    print("ERROR: Cost must be symmetric!")
                    raise Exception

    def __str__(self) -> str:
        return super().__str__() + f"\nWeights: {self.cost_dict}"

    def induced_graph(self, vertices: List[int]):
        """
            Returns the graph induced by the input vertices.
        """
        if max(vertices) >= self.number_of_vertices:
            print("ERROR: Input vertices must be in the graph!")
            raise Exception
        induced_number_of_vertices = len(vertices)
        induced_adj_matrix = [[False for _ in range(induced_number_of_vertices)]
                              for _ in range(induced_number_of_vertices)]
        induced_cost_dict: Dict[Tuple[int, int], float] = {}
        for i in range(induced_number_of_vertices):
            for j in range(induced_number_of_vertices):
                v, w = vertices[i], vertices[j]
                if self.adj_matrix[v][w]:
                    induced_adj_matrix[i][j] = True
                    induced_cost_dict[(i, j)] = self.cost_dict[(v, w)]
        return WeightedGraph(induced_number_of_vertices, induced_adj_matrix, induced_cost_dict)

    def cost(self, edges: Set[Tuple[int, int]]):
        """
            Returns the sum of the cost of the input edges. If an input edge does not
            belong to the graph, an Exception is raised.
        """
        for edge in edges:
            if edge not in self.edges():
                print(
                    "ERROR: Cannot calculate cost of edge {edge} since it's not in the graph.")
                raise Exception
        return sum([self.cost_dict[edge] for edge in edges])

    def remove_vertice(self, vertice: int):
        """
            Returns a new weighted graph without the input vertice.
        """
        if vertice not in self.vertices():
            return Graph(self.number_of_vertices, self.adj_matrix)
        number_of_vertices = self.number_of_vertices - 1
        adj_matrix = [[self.adj_matrix[v][w]
                       for v in self.vertices() if v != vertice]
                      for w in self.vertices() if w != vertice]
        for v in range(len(self.vertices())-1):
            if len(adj_matrix[v]) != len(self.vertices())-1:
                print(f"ERROR: Resulting matrix after " +
                      f"removing vertice {vertice} is wrong.")
                raise Exception
        cost_dict: Dict[Tuple[int, int], float] = {}
        for v, w in self.cost_dict.keys():
            if v == vertice or w == vertice:
                continue
            new_v = v if v < vertice else (v-1)
            new_w = w if w < vertice else (w-1)
            cost_dict[(new_v, new_w)] = self.cost_dict[(v, w)]
        return WeightedGraph(number_of_vertices, adj_matrix, cost_dict)

    def remove_edges(self, edges: Set[Tuple[int, int]]):
        """
            Returns a new graph without the specified edges.
        """
        for v, w in edges:
            if v >= self.number_of_vertices or w >= self.number_of_vertices:
                print("ERROR: Vertices don't exist!")
                raise Exception
        adj_matrix = [[self.adj_matrix[v][w]
                       for v in self.vertices()] for w in self.vertices()]
        for v, w in edges:
            adj_matrix[v][w] = False
        return WeightedGraph(self.number_of_vertices, adj_matrix, self.cost_dict.copy())


class EuclideanCompleteWeightedGraph(WeightedGraph):

    def __init__(
        self,
        coordinates: List[Tuple[float, float]]
    ):
        self.coordinates = coordinates
        number_of_vertices = len(coordinates)
        vertices = [i for i in range(number_of_vertices)]
        adj_matrix = [[True if i != j else False for i in vertices]
                      for j in vertices]
        cost_dict = {}
        for v in vertices:
            for w in vertices:
                if v == w:
                    continue
                v_pos = self.coordinates[v]
                w_pos = self.coordinates[w]
                cost_dict[(v, w)] = \
                    math.sqrt((v_pos[0]-w_pos[0])**2 + (v_pos[1]-w_pos[1])**2)
        super().__init__(number_of_vertices, adj_matrix, cost_dict)

    def render(
        self,
        screen,
        vertice_color: Tuple[int, int, int] = (0, 0, 0),
        edge_color: Tuple[int, int, int] = (220, 220, 220),
        render_indexes: bool = False
    ):
        """
            Renders the whole graph on the screen according to the coordinates.
        """
        font = pygame.font.SysFont('Arial', 20)
        for v in self.vertices():
            for w in self.vertices():
                pygame.draw.line(screen, edge_color,
                                 self.coordinates[v], self.coordinates[w], 3)
        for v in self.vertices():
            pygame.draw.circle(screen, vertice_color, self.coordinates[v], 5)
            if not render_indexes:
                continue
            text_surface = font.render(str(v), False, (0, 0, 0))
            screen.blit(
                text_surface, (self.coordinates[v][0]-20, self.coordinates[v][1]-20))

    def render_edges(
        self,
        screen,
        edges: List[Tuple[int, int]],
        vertice_color: Tuple[int, int, int] = (0, 0, 255),
        edge_color: Tuple[int, int, int] = (0, 0, 255)
    ):
        """
            Renders only the specified input edges and the corresponding vertices
            based on the coordinates. If the input is not a subset of the graph edges,
            raises an Exception.
        """
        for edge in edges:
            if edge not in self.edges():
                print("ERROR: Input must be a subset of the graph's edges.")
                raise Exception
        for v, w in edges:
            pygame.draw.line(screen, edge_color,
                             self.coordinates[v], self.coordinates[w], 3)
        for v, w in edges:
            pygame.draw.circle(screen, vertice_color, self.coordinates[v], 5)
            pygame.draw.circle(screen, vertice_color, self.coordinates[w], 5)

    def translate(self, delta: Tuple[float, float]):
        """
            Translates the graph by the input delta vector and returns a new graph.
        """
        translated_coordinates: List[Tuple[float, float]] = [
            (x + delta[0], y + delta[1]) for x, y in self.coordinates
        ]
        return EuclideanCompleteWeightedGraph(translated_coordinates)


class RandomEuclideanCompleteWeightedGraph(EuclideanCompleteWeightedGraph):
    def __init__(
        self,
        number_of_vertices: int,
        interval_x: Tuple[float, float] = (0.0, 1.0),
        interval_y: Tuple[float, float] = (0.0, 1.0)
    ):
        coordinates = [(random.uniform(interval_x[0], interval_x[1]),
                        random.uniform(interval_y[0], interval_y[1]))
                       for _ in range(number_of_vertices)]
        super().__init__(coordinates)
