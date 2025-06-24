# Generates coordinates of dodecahedron
# https://stackoverflow.com/questions/10460337/how-to-generate-calculate-vertices-of-dodecahedron
import math
import json
from dataclasses import dataclass
import pygame as pg

SCALE = 250

@dataclass
class Node:
    index: int
    edges: list[int]
    vector: pg.Vector3


phi = (1 + math.sqrt(5)) / 2

coords: list[pg.Vector3] = []
plus_or_minus = (-1, 1)

# cube
for x in plus_or_minus:
    for y in plus_or_minus:
        for z in plus_or_minus:
            coords.append(pg.Vector3(x, y, z))

for a in plus_or_minus:
    for b in plus_or_minus:
        coords.append(pg.Vector3(0, a / phi, b * phi))
        coords.append(pg.Vector3(a / phi, b * phi, 0))
        coords.append(pg.Vector3(a * phi, 0, b / phi))

edge_length = 2 / phi


nodes: list[Node] = []
for i, a in enumerate(coords):
    edges = []
    for j, b in enumerate(coords):
        if i == j:
            continue
        if abs(a.distance_to(b) - edge_length) < 1e-2:
            edges.append(j)

    nodes.append(Node(i, edges, a))


# export nodes to JSON

with open("dodecahedron.json", "w") as fp:
    json.dump(
        [
            {"location": node.index, "tunnels": node.edges, "coords": list(node.vector * SCALE)}
            for node in nodes
        ],
        fp,
    )
