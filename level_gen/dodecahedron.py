# Generates coordinates of dodecahedron
# https://stackoverflow.com/questions/10460337/how-to-generate-calculate-vertices-of-dodecahedron
import math
from .common import Node, dump, graph_from_edge_length
import numpy.typing as npt
import numpy as np

phi = (1 + math.sqrt(5)) / 2

coords: list[npt.NDArray] = []
plus_or_minus = (-1, 1)

# cube
for x in plus_or_minus:
    for y in plus_or_minus:
        for z in plus_or_minus:
            coords.append(np.array([x, y, z]))

for a in plus_or_minus:
    for b in plus_or_minus:
        coords.append(np.array([0, a / phi, b * phi]))
        coords.append(np.array([a / phi, b * phi, 0]))
        coords.append(np.array([a * phi, 0, b / phi]))

edge_length = 2 / phi


dump(graph_from_edge_length(coords, edge_length, 1e-2), "dodecahedron.json")
