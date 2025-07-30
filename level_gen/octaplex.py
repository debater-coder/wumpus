import numpy as np
import numpy.typing as npt
from .common import dump, graph_from_edge_length
import math

coords: list[npt.NDArray] = []
plus_or_minus = (-1, 1)

for a in plus_or_minus:
    for b in plus_or_minus:
        coords.append(np.array([a, b, 0, 0]))
        coords.append(np.array([a, 0, b, 0]))
        coords.append(np.array([a, 0, 0, b]))
        coords.append(np.array([0, a, b, 0]))
        coords.append(np.array([0, a, 0, b]))
        coords.append(np.array([0, 0, a, b]))


dump(graph_from_edge_length(coords, math.sqrt(2), 1e-2), "octaplex.json")
