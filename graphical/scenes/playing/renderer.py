from kingdon import Algebra
import numpy as np
import numpy.typing as npt
import typing

from wumpus.level import Level


class Renderer:
    """
    Renders a level of abitrary dimension to 2D.
    Yields events for player interactions.
    The image plane is parallel to the first two basis vectors (eg: xy)
    with its last coordinate (eg: z) changing to zoom."""

    def __init__(self, level: Level):
        self.level = level
        dimension = len(list(self.level.level.values())[0].coords)
        self.algebra = Algebra(dimension)

        # positions camera at (0, 0, 0, ..., -5)
        self.camera_pos = self.algebra.vector(np.array([0] * (dimension - 1) + [-5]))

    def perp_dist(self, coord: npt.NDArray) -> float:
        perpendicular = coord[2:]
        return typing.cast(float, np.linalg.norm(perpendicular))
