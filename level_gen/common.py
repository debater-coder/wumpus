import json
from dataclasses import dataclass
import numpy as np
import numpy.typing as npt
import math


@dataclass
class Node:
    index: int
    edges: list[int]
    vector: npt.NDArray


def graph_from_edge_length(
    coords: list[npt.NDArray], edge_length: float, tolerance: float
) -> list[Node]:
    """
    Generates a graph from a list of points, where two nodes
    are joined by an edge only when it is within a tolerance
    of a given edge length.
    """
    nodes: list[Node] = []

    for i, a in enumerate(coords):
        edges = []
        for j, b in enumerate(coords):
            if i == j:
                continue
            if abs(math.sqrt(np.dot((b - a), (b - a))) - edge_length) < 1e-2:
                edges.append(j)

        nodes.append(Node(i, edges, a))

    return nodes


def dump(nodes: list[Node], file: str):
    """Exports nodes to JSON"""
    with open(file, "w") as fp:
        json.dump(
            [
                {
                    "location": node.index,
                    "tunnels": node.edges,
                    "coords": list(map(float, (node.vector))),
                }
                for node in nodes
            ],
            fp,
        )
