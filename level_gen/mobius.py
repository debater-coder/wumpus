import math
from .common import dump, Node
import numpy.typing as npt
import numpy as np

EDGE_LENGTH = 16

top_edge: list[npt.NDArray] = []
bottom_edge: list[npt.NDArray] = []


def points(u: float, v: float):
    return np.array(
        [
            (1 + v / 2 * math.cos(u / 2)) * math.cos(u),
            (1 + v / 2 * math.cos(u / 2)) * math.sin(u),
            v / 2 * math.sin(u / 2),
        ]
    )


for i in range(EDGE_LENGTH):
    top_edge.append(points(i * 2 * math.pi / EDGE_LENGTH, 1))
    bottom_edge.append(points(i * 2 * math.pi / EDGE_LENGTH, -1))

nodes: list[Node] = []

# middle part of mobius strip
for index, (top, bottom) in enumerate(zip(top_edge[1:-1], bottom_edge[1:-1])):
    i = index + 1  # (0 and 1 are reserved)
    nodes.append(
        Node(
            i * 2,
            [
                i * 2 + 1,  # bottom
                (i - 1) * 2,  # before
                (i + 1) * 2,  # after
            ],
            top,
        )
    )

    nodes.append(
        Node(
            i * 2 + 1,
            [
                i * 2,  # top
                (i - 1) * 2 + 1,  # before
                (i + 1) * 2 + 1,  # after
            ],
            bottom,
        )
    )

# special nodes (the crossover)
nodes.append(
    Node(
        0,
        [
            1,  # bottom
            EDGE_LENGTH * 2 - 1,  # before
            2,  # after
        ],
        top_edge[0],
    )
)

nodes.append(
    Node(
        1,
        [
            0,  # top
            EDGE_LENGTH * 2 - 2,  # before
            3,  # after
        ],
        bottom_edge[0],
    )
)

nodes.append(
    Node(
        EDGE_LENGTH * 2 - 2,
        [
            EDGE_LENGTH * 2 - 1,  # bottom
            EDGE_LENGTH * 2 - 4,  # before
            1,  # after
        ],
        top_edge[-1],
    )
)

nodes.append(
    Node(
        EDGE_LENGTH * 2 - 1,
        [
            EDGE_LENGTH * 2 - 2,  # top
            EDGE_LENGTH * 2 - 3,  # before
            2,  # after
        ],
        bottom_edge[-1],
    )
)

dump(nodes, "mobius.json")
