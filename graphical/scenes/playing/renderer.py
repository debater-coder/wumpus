from kingdon import Algebra, MultiVector
import numpy as np
import numpy.typing as npt
import pygame as pg
import math

from wumpus import Level, Cave

from graphical.colours import COLOURS
from graphical.utils import apply_fade, load_and_recolor_icon
import graphical.icons

from .drawable import RenderContext
from .cave import DrawableCave, DrawablePlayer
from .drawable import Drawable


class Renderer:
    """
    Renders a level of abitrary dimension to 2D.
    Yields events for player interactions.
    The image plane is parallel to the first two basis vectors (eg: xy)
    with its third (eg: z) changing to zoom.
    """

    def __init__(self, level: Level, fov: float = 90):
        self.level = level
        self.fov = fov
        self.dimension = len(list(self.level.level.values())[0].coords)
        self.algebra = Algebra(self.dimension)  # Clifford algebra

        self.basis_vectors = list(
            filter(
                lambda blade: blade[1].grades[0] == 1, list(self.algebra.blades.items())
            )
        )  # get grade 1 blades

        self.reset_rotor()
        self.reset_zoom()

        self.load_icons()

    def reset_zoom(self):
        """positions camera at (0, 0, -5, 0, 0, ...)"""
        self.camera_pos = np.array([0, 0, -5] + [0] * (self.dimension - 3))

    def reset_rotor(self):
        self.rotor = self.algebra.scalar(np.array([1]))
        if self.dimension == 4:
            self.rotate(
                self.basis_vectors[3][1] ^ self.basis_vectors[0][1], math.pi / 4
            )
            self.rotate(
                self.basis_vectors[3][1] ^ self.basis_vectors[1][1], math.pi / 4
            )
            self.rotate(
                self.basis_vectors[3][1] ^ self.basis_vectors[2][1], math.pi / 4
            )

    def rotate(self, bivector: MultiVector, angle: float):
        """Rotate on bivector by angle."""
        self.rotor = (
            (bivector.grade(2).normalized() * angle / 2).exp() * self.rotor
        ).normalized()

    def zoom(self, value: float):
        """Moves camera on the 'z'-axis by `value`."""
        self.camera_pos[2] += value

    def perp_dist(self, coord: npt.NDArray) -> float:
        """
        Get the perpendicular distance between the image plane and object.
        In 4D and above there are more than one directions perpendicuar to any
        2D plane. We define our camera orientation to look down the third-axis

        Used for foreshortening.

        Originally, I thought the perpendicular distance should be the
        length of the component of the vector perpendicular to the image
        plane. This is not the case, forshortening only applies in the
        direction parallel to your line of sight. Consider a 1D image
        line in a 3D space. A single axis is chosen for an image line,
        but the direction of sight has more than one option
        (in 3D there are infinitely many vectors perependicular to a vector).
        Thus a perpendicuar direction (line of sight) must be chosen.
        """
        return (coord - self.camera_pos)[2]

    def vector_from_multivector(self, mv: MultiVector):
        """Extracts a numpy array from the vector part of a multivector"""
        return np.array([getattr(mv, basis[0]) for basis in self.basis_vectors])

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

    def apply_depth_fade(self, color, coords: npt.NDArray) -> pg.Color:
        """
        Apply depth-based darkening to a color for arbitrary-dimensional rendering.

        Args:
            color: Base color (RGB tuple or pygame Color)
            coords: N-dimensional coordinates where the third component is depth along line of sight

        Returns:
            Color darkened based on depth
        """
        depth_fade = max(0, min(0.5, coords[2]))
        return apply_fade(color, 1.0 - depth_fade)

    def load_icons(self):
        self.pit_icon = load_and_recolor_icon(
            graphical.icons, "pit.png", COLOURS["green_400"]
        )
        self.bat_icon = load_and_recolor_icon(
            graphical.icons, "bat.png", COLOURS["blue_400"]
        )
        self.wumpus_icon = load_and_recolor_icon(
            graphical.icons, "wumpus.png", COLOURS["red_400"]
        )
        self.player_icon = load_and_recolor_icon(
            graphical.icons, "player.png", COLOURS["yellow_400"]
        )

    def create_drawables(
        self,
        player_location: int | None,
        hovered_cave: int | None,
        shooting_path: list[int],
        explored: set[int],
        near_wumpus: set[int],
        show_wumpus: bool
    ) -> list[Drawable]:
        """Create all drawable objects for the level."""
        drawables = []

        for cave_location in explored:
            is_hovered = cave_location == hovered_cave
            is_in_shooting_path = cave_location in shooting_path
            cave = self.level.get_cave(cave_location)
            drawable_cave = DrawableCave(
                cave=cave,
                explored=True,
                is_hovered=is_hovered,
                is_in_shooting_path=is_in_shooting_path,
                near_wumpus=cave_location in near_wumpus,
                show_wumpus=show_wumpus
            )
            drawables.append(drawable_cave)

            for adjacent_cave_location in cave.tunnels:
                if adjacent_cave_location in explored:
                    continue

                is_hovered = adjacent_cave_location == hovered_cave
                is_in_shooting_path = adjacent_cave_location in shooting_path
                adjacent_cave = self.level.get_cave(adjacent_cave_location)
                drawable_cave = DrawableCave(
                    cave=adjacent_cave,
                    explored=False,
                    is_hovered=is_hovered,
                    is_in_shooting_path=is_in_shooting_path,
                )
                drawables.append(drawable_cave)

        if player_location is not None:
            player_cave = self.level.get_cave(player_location)
            drawable_player = DrawablePlayer(cave=player_cave)
            drawables.append(drawable_player)

        return drawables

    def draw_icon(
        self,
        surf: pg.surface.Surface,
        icon: pg.surface.Surface | None,
        size: int,
        opacity: int,
        center: pg.Vector2,
    ):
        if not icon:
            return
        scaled_icon = pg.transform.scale(icon, (size, size))

        icon_with_alpha = scaled_icon.copy()
        icon_with_alpha.set_alpha(opacity)

        icon_rect = icon_with_alpha.get_rect(center=center)
        surf.blit(icon_with_alpha, icon_rect)

    def paint(
        self,
        surf: pg.surface.Surface,
        location: int | None,
        mouse_pos: pg.Vector2,
        shooting_path: list[int],
        explored: set[int],
        near_wumpus: set[int],
        show_wumpus: bool
    ):
        """Draws level to screen."""
        context = RenderContext(self, self.level)

        hovered_cave = self.get_cave_at_pos(mouse_pos)
        drawables = self.create_drawables(
            location,
            hovered_cave.location if hovered_cave else None,
            shooting_path,
            explored,
            near_wumpus,
            show_wumpus
        )

        # Sort by depth (farthest first) so closer objects render on top
        # Objects with larger perpendicular distance along the third basis are farther away
        # Reverse=True means farthest objects are drawn first (painter's algorithm)
        drawables.sort(
            key=lambda drawable: self.perp_dist(self.rotated(drawable.get_coords())),
            reverse=True,
        )

        self._draw_tunnels(surf, explored)

        for drawable in drawables:
            drawable.paint(surf, context)

    def get_cave_at_pos(self, pos: pg.Vector2) -> "Cave | None":
        """Get the cave at a given position on the screen."""
        for cave in self.level.level.values():
            coords = self.rotated(np.array(cave.coords))
            center = self.project(coords, pg.display.get_surface())
            radius = 100 / max(self.perp_dist(coords), 1e-6)

            if pos.distance_to(center) <= radius:
                return cave
        return None

    def _draw_tunnels(self, surf: pg.surface.Surface, explored: set[int]):
        """Draw all tunnel connections between caves."""
        drawn = set()
        caves = self.level.level

        for cave in [caves[location] for location in explored]:
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
