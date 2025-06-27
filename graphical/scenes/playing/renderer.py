from kingdon import Algebra, MultiVector
import numpy as np
import numpy.typing as npt
import pygame as pg
import math

from wumpus.hazards import BottomlessPit, Superbats, Wumpus
from wumpus.level import Level

from graphical.colours import COLOURS
from graphical.utils import apply_fade


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

        self.basis_vectors = list(
            filter(lambda blade: blade[1].grades[0] == 1, list(self.algebra.blades.items()))
        )  # get grade 1 blades

        self.reset_rotor()
        self.reset_zoom()

        # Load hazard icons
        self.load_icons()

    def reset_zoom(self):
        """positions camera at (0, 0, 0, ..., -5)"""
        self.camera_pos = np.array([0] * (self.dimension - 1) + [-5])

    def reset_rotor(self):
        self.rotor = self.algebra.scalar(np.array([1]))

    def rotate(self, bivector: MultiVector, angle: float):
        """Rotate on bivector by angle."""
        self.rotor = ((bivector.grade(2).normalized() * angle/2).exp() * self.rotor).normalized()

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
        (in 3D there are infinitely many vectors perependicular to a vector).
        Thus a perpendicuar direction (line of sight) must be chosen.
        """
        return (coord - self.camera_pos)[-1]

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
        Apply depth-based darkening to a color for 3D rendering effects.

        Args:
            color: Base color (RGB tuple or pygame Color)
            coords: 3D coordinates where the last component is depth (z-axis)

        Returns:
            Color darkened based on depth
        """
        depth_fade = max(0, min(0.5, coords[-1]))
        return apply_fade(color, 1.0 - depth_fade)

    def load_icons(self):
        """Load hazard icons from files."""
        self.pit_icon = None
        self.bat_icon = None

        original_wumpus = pg.image.load("graphical/icons/wumpus.png").convert_alpha()
        # Create white version by creating a white surface and using the original as a mask
        self.wumpus_icon = pg.Surface(original_wumpus.get_size(), pg.SRCALPHA)
        # Use the original image's alpha channel to cut out the shape
        mask = pg.mask.from_surface(original_wumpus)
        mask_surface = mask.to_surface(setcolor=COLOURS["red_400"], unsetcolor=(0, 0, 0, 0))
        self.wumpus_icon = mask_surface
        print(self.wumpus_icon)

    def draw_cave(self, surf: pg.surface.Surface, cave, coords: npt.NDArray, explored: bool = True):
        """Draw a single cave with hazard indicators."""
        # Skip caves that are behind the camera
        if self.perp_dist(coords) <= 0:
            return

        center = pg.Vector2(self.project(coords, surf))
        radius = 100 / self.perp_dist(coords)

        nearby_hazards = self.level.get_nearby_hazards(cave)
        has_nearby_pit = any(isinstance(hazard, BottomlessPit) for hazard in nearby_hazards)
        has_nearby_bats = any(isinstance(hazard, Superbats) for hazard in nearby_hazards)
        has_nearby_wumpus = any(isinstance(hazard, Wumpus) for hazard in nearby_hazards)

        outline_layers = []

        if has_nearby_pit:
            outline_layers.append((COLOURS["green_500"], radius + 10))

        if has_nearby_bats:
            outline_layers.append((COLOURS["blue_500"], radius + 5))

        if not has_nearby_pit and not has_nearby_bats:
            outline_layers.append((COLOURS["zinc_600"], radius + 5))

        for color, layer_radius in outline_layers:
            tinted_color = self.apply_depth_fade(color, coords)
            pg.draw.circle(surf, tinted_color, center, layer_radius)

        if explored:
            interior_color = COLOURS["zinc_950"]
        else:
            interior_color = COLOURS["zinc_600"]

        # Draw main cave circle
        tinted_interior = self.apply_depth_fade(interior_color, coords)
        pg.draw.circle(surf, tinted_interior, center, radius)

        if has_nearby_wumpus:
            wumpus_radius = radius * 2 / 3
            tinted_orange = self.apply_depth_fade(COLOURS["orange_500"], coords)
            pg.draw.circle(surf, tinted_orange, center, wumpus_radius)

        # Draw hazard icons inside caves containing hazards
        hazard_in_cave = self.level.get_hazard_in_cave(cave)
        if hazard_in_cave is not None:
            icon = None
            if isinstance(hazard_in_cave, BottomlessPit) and self.pit_icon:
                icon = self.pit_icon
            elif isinstance(hazard_in_cave, Superbats) and self.bat_icon:
                icon = self.bat_icon
            elif isinstance(hazard_in_cave, Wumpus) and self.wumpus_icon:
                icon = self.wumpus_icon

            if icon:
                icon_size = int(radius)  # 80% of cave diameter
                scaled_icon = pg.transform.scale(icon, (icon_size, icon_size))

                # Apply depth-based opacity to icon
                opacity = 255 - int(255 * max(0, min(0.5, coords[-1])))
                icon_with_alpha = scaled_icon.copy()
                icon_with_alpha.set_alpha(opacity)

                icon_rect = icon_with_alpha.get_rect(center=center)
                surf.blit(icon_with_alpha, icon_rect)

    def paint(self, surf: pg.surface.Surface):
        """Draws level to screen."""
        drawn = set()

        for cave in sorted(
            (caves := self.level.level).values(),
            key=lambda cave: self.perp_dist(self.rotated(np.array(cave.coords))),
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

            self.draw_cave(surf, cave, coords, explored=True)
