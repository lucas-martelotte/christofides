from typing import Set, Tuple
import pygame
import math

from graph import EuclideanCompleteWeightedGraph


def remove_edge_pairs(edges: Set[Tuple[int, int]]):
    """
        For every pair (v,w), (w,v) in the set, the algorithm removes one of
        the elements of the pair and keeps the other one.
    """
    new_edges: Set[Tuple[int, int]] = set()
    for e in edges:
        if (e[1], e[0]) not in new_edges:
            new_edges.add(e)
    return new_edges


'''
def remove_hourglasses(graph: EuclideanCompleteWeightedGraph, edges: Set[Tuple[int, int]]):
    """
        Receives an euclidean graph and a subset of its edges. Every time an edge
        intersects with another in the plane, the algorithm "removes" the intersection
        by substituting these edges by others with less weight.
    """
    new_edges = [e for e in edges]
    for v_1, v_2 in edges:
        for w_1, w_2 in edges:
            if len(set([v_1, v_2, w_1, w_2])) != 4:  # edges can't meet
                continue
            pv_1 = graph.coordinates[v_1]
            pv_2 = graph.coordinates[v_2]
            pw_1 = graph.coordinates[w_1]
            pw_2 = graph.coordinates[w_2]
            if intersect(pv_1, pv_2, pw_1, pw_2):
                print(f"{(v_1, v_2)} intersects with {(w_1, w_2)}.")
                try:
                    new_edges.remove((v_1, v_2))
                    new_edges.remove((w_1, w_2))
                    new_edges.append((v_1, w_2))
                    new_edges.append((w_1, v_2))
                except:
                    pass
    return set(new_edges)


def ccw(A, B, C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if line segments AB and CD intersect


def intersect(A, B, C, D):
    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
'''
