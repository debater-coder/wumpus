from kingdon import Algebra, MultiVector
import numpy as np
import numpy.typing as npt
import pygame as pg
import typing
import math

from wumpus.level import Level

from graphical.colours import COLOURS


class Renderer:
    """
    Renders a level of abitrary dimension to 2D.
    Yields events for player interactions.
    The image plane is parallel to the first two basis vectors (eg: xy)
    with its last coordinate (eg: z) changing to zoom."""

    def __init__(self, level: Level, fov: float = 90):
        self.level = level
        self.fov = fov
        self.dimension = len(list(self.level.level.values())[0].coords)
        self.algebra = Algebra(self.dimension)  # Clifford algebra
        self.rotor = self.algebra.scalar(np.array([1]))

        self.reset_zoom()

    def reset_zoom(self):
        """positions camera at (0, 0, 0, ..., -5)"""
        self.camera_pos = np.array([0] * (self.dimension - 1) + [-5])

    def zoom(self, value: float):
        """Moves camera on the 'z'-axis by `value`."""
        self.camera_pos[-1] += value

    def perp_dist(self, coord: npt.NDArray) -> float:
        """
        Get the perpendicular distance between the image plane and object.
        In 4D and above there are more than one directions perpendicuar to any
        2D plane. We define our camera orientation to look down the 'z'-axis
        (the last coordinate).

        Used for foreshortening.

        Originally, I thought the perpendicular distance should be the
        length of the component of the vector perpendicular to the image
        plane. This is not the case, forshortening only applies in the
        direction parallel to your line of sight. Consider a 1D image
        line in a 3D space. A single axis is chosen for an image line,
        but the direction of sight has more than one option
        (in 3D there are infinitely many vectors perependicuar to a vector).
        Thus a perpendicuar direction (line of sight) must be chosen.
        """
        return (coord - self.camera_pos)[-1]

    def vector_from_multivector(self, mv: MultiVector):
        """Extracts a numpy array from the vector part of a multivector"""
        basis_vectors = list(
            filter(lambda blade: blade[1].grades[0] == 1, list(self.algebra.blades.items()))
        )  # get grade 1 blades

        return np.array([getattr(mv, basis[0]) for basis in basis_vectors])

    def project(self, coord: npt.NDArray, screen) -> pg.Vector2:
        """Projects an arbritrary dimension vector onto the image plane."""
        planar = coord[:2]  # component of cooridnate parallel to image plane
        return (
            pg.Vector2(*planar)
            * screen.get_rect().height
            / max(
                1e-3, self.perp_dist(coord) * math.tan(math.radians(self.fov / 2))
            )  # scale it by perpendicular distance to image plane
            + pg.Vector2(1920, 1080) / 2  # center on screen
        )

    def rotated(self, coord: npt.NDArray) -> npt.NDArray:
        """Get the roated nD coordinates of a coordinate."""
        return self.vector_from_multivector(self.rotor >> self.algebra.vector(coord))

    def paint(self, surf: pg.surface.Surface):
        drawn = set()

        for cave in sorted(
            (caves := self.level.level).values(),
            key=lambda cave: self.perp_dist(np.array(cave.coords)),
            reverse=True,
        ):
            coords = self.rotated(np.array(cave.coords))
            for edge in cave.tunnels:
                edge_coords = self.rotated(np.array(caves[edge].coords))
                if (cave.location, edge) in drawn:
                    continue
                pg.draw.line(
                    surf,
                    COLOURS["zinc_50"],
                    pg.Vector2(self.project(edge_coords, surf)),
                    pg.Vector2(self.project(coords, surf)),
                )
                drawn.add((edge, cave.location))

            pg.draw.circle(
                surf,
                pg.Color(COLOURS["amber_900"]).lerp(
                    (0, 0, 0, 0), max(0, min(0.5, coords[-1]))
                ),
                pg.Vector2(self.project(coords, surf)),
                100 / self.perp_dist(coords),
            )
