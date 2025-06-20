from dataclasses import dataclass
import pygame as pg
import math


@dataclass
class Node:
    index: int
    edges: list[int]
    vector: pg.Vector2

def force_directed_layout(graph: dict[int, Node], iterations=1000, step=0.05):
    k = math.sqrt(1920 * 1080 / len(graph))

    for _ in range(iterations):
        for node in graph.values():
            force = pg.Vector2(0, 0)

            # repulsion (all other nodes)
            for other in filter(lambda n: n.index != node.index, graph.values()):
                distance = max(node.vector.distance_to(other.vector), 1e-4)
                direction = other.vector - node.vector
                direction.normalize_ip()

                force += (-(k*k)/distance) * direction

            # attraction (edges)
            for other in (graph[i] for i in node.edges):
                distance = max(node.vector.distance_to(other.vector), 1e-4)
                direction = other.vector - node.vector
                direction.normalize_ip()

                force += ((distance*distance)/k) * direction

            node.vector += step * force
