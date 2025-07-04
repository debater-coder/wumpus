import numpy as np
import numpy.typing as npt
from .common import dump, graph_from_edge_length

coords: list[npt.NDArray] = []
plus_or_minus = (-1, 1)

for w in plus_or_minus:
    for x in plus_or_minus:
        for y in plus_or_minus:
            for z in plus_or_minus:
                coords.append(np.array([w, x, y, z]))


dump(graph_from_edge_length(coords, 2, 1e-2), "tesseract.json")
