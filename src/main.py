from typing import List, Tuple

import pygame
import numpy as np
import math

from graph import RandomEuclideanCompleteWeightedGraph
from utils import remove_edge_pairs  # , remove_hourglasses
from lower_bound_1_tree import LowerBound1Tree
from mwpm import MinimumWeightPerfectMatching
from euler import EulerCycle
from kruskal import Kruskal


screen_width, screen_height = 1500, 800

pygame.init()
pygame.font.init()
pygame.display.set_caption('Christofides')
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
default_font = pygame.font.SysFont('Arial', 28)

# Constants
number_of_vertices = 12
max_ratios_to_be_stored = 60
# Global variables
graph = None  # type: ignore
translated_graph_1 = None  # type: ignore
translated_graph_2 = None  # type: ignore
minimum_spanning_tree = None  # type: ignore
minimum_perfect_matching = None  # type: ignore
tsp_cycle = None  # type: ignore
tsp_cycle_cost = None  # type: ignore
max_one_tree = None  # type: ignore
max_one_tree_cost = None  # type: ignore
current_ratio = 0.0
average_ratio = 0.0
ratios: List[float] = []
iterations = 0


def reset_graph():
    global graph, translated_graph_1, translated_graph_2, \
        minimum_spanning_tree, minimum_perfect_matching, \
        tsp_cycle, tsp_cycle_cost, max_one_tree, max_one_tree_cost, \
        current_ratio, average_ratio, ratios, iterations
    graph = RandomEuclideanCompleteWeightedGraph(
        number_of_vertices=number_of_vertices,
        interval_x=(20, screen_width//3 - 20),
        interval_y=(20, screen_height - 220)
    )
    translated_graph_1 = graph.translate((screen_width//3, 0))
    translated_graph_2 = graph.translate((2*screen_width//3, 0))
    max_one_tree, max_one_tree_cost =\
        LowerBound1Tree(graph).get_maximum_1_tree()
    #========================================================================#
    #========== MINIMUM SPANNING TREE AND MINIMUM PERFECT MATCHING ==========#
    #========================================================================#
    minimum_spanning_tree = Kruskal(graph).minimum_spanning_tree()
    odd_degree_vertices = \
        [v for v in graph.vertices()
         if sum([1 if v == e[0] else 0 for e in minimum_spanning_tree]) in [1, 3]]
    induced_minimum_perfect_maching = MinimumWeightPerfectMatching(
        graph.induced_graph(odd_degree_vertices)).minimum_weight_perfect_matching()
    minimum_perfect_matching = set([(odd_degree_vertices[v], odd_degree_vertices[w])
                                    for v, w in induced_minimum_perfect_maching])
    #========================================================================#
    #=========== CALCULATING EULER CYCLE AND REMOVING DUPLICATES ============#
    #========================================================================#
    euler_cycle = EulerCycle(list(remove_edge_pairs(minimum_spanning_tree)) +
                             list(minimum_perfect_matching)
                             ).euler_cycle()
    tsp_cycle_vertices: List[int] = []
    for v in euler_cycle:
        if v not in tsp_cycle_vertices:
            tsp_cycle_vertices.append(v)
    tsp_cycle_vertices.append(tsp_cycle_vertices[0])
    tsp_cycle = []
    for i in range(len(tsp_cycle_vertices)-1):
        tsp_cycle.append(
            (tsp_cycle_vertices[i], tsp_cycle_vertices[i+1])
        )
    tsp_cycle_cost = graph.cost(tsp_cycle)
    current_ratio = tsp_cycle_cost/max_one_tree_cost
    average_ratio = (iterations*(average_ratio) + current_ratio)/(iterations+1)
    ratios.append(current_ratio)
    if len(ratios) > max_ratios_to_be_stored:
        ratios.pop(0)
    iterations += 1


def draw():
    screen.fill((255, 255, 255))
    graph.render(screen)
    graph.render_edges(screen, max_one_tree,
                       vertice_color=(150, 0, 205), edge_color=(150, 0, 205))
    translated_graph_1.render(screen)
    translated_graph_1.render_edges(screen, minimum_spanning_tree)
    translated_graph_1.render_edges(screen, minimum_perfect_matching,
                                    edge_color=(255, 0, 0))
    translated_graph_2.render(screen, render_indexes=True)
    translated_graph_2.render_edges(screen, tsp_cycle,
                                    edge_color=(0, 0, 100))
    pygame.draw.rect(screen, (0, 0, 0),
                     [0, screen_height-200, screen_width, 3])
    text = default_font.render(
        f"COST: {round(tsp_cycle_cost,2)}", False, (0, 0, 0))
    text_rect = text.get_rect(midright=(screen_width-10, screen_height-180))
    screen.blit(text, text_rect)
    text = default_font.render(
        f"1-TREE: {round(max_one_tree_cost,2)}", False, (0, 0, 0))
    text_rect = text.get_rect(midright=(screen_width-10, screen_height-150))
    screen.blit(text, text_rect)
    text = default_font.render(
        f"CURRENT RATIO: {round(current_ratio,2)}", False, (0, 0, 0))
    text_rect = text.get_rect(midright=(screen_width-10, screen_height-80))
    screen.blit(text, text_rect)
    text = default_font.render(
        f"AVERAGE RATIO: {round(average_ratio,2)}", False, (0, 0, 0))
    text_rect = text.get_rect(midright=(screen_width-10, screen_height-50))
    screen.blit(text, text_rect)
    text = default_font.render(
        f"ITERATIONS: {iterations}", False, (0, 0, 0))
    text_rect = text.get_rect(midright=(screen_width-10, screen_height-20))
    screen.blit(text, text_rect)
    step_width = (screen_width-350)/max_ratios_to_be_stored
    for i in range(len(ratios)-1):
        pygame.draw.line(screen, (0, 0, 255),
                         (step_width*i, screen_height-100*ratios[i]),
                         (step_width*(i+1), screen_height-100*ratios[i+1]), 5)
    pygame.draw.line(screen, (0, 255, 0),
                     (0, screen_height-100),
                     ((max_ratios_to_be_stored-1)*step_width, screen_height-100))
    pygame.draw.line(screen, (255, 0, 0),
                     (0, screen_height-150),
                     ((max_ratios_to_be_stored-1)*step_width, screen_height-150))
    pygame.display.update()


reset_graph()

while True:
    clock.tick(30)
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            reset_graph()
        if event.type == pygame.MOUSEBUTTONUP:
            pass
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                pass
