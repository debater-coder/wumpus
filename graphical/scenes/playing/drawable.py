"""
Drawable architecture for arbitrary-dimensional rendering in the Wumpus game.

This module provides the foundation for object-oriented rendering where each
game object (caves, player, etc.) is responsible for its own drawing logic.
The architecture uses a Drawable pattern with depth sorting to ensure proper
rendering order using the painter's algorithm.

The renderer projects arbitrary-dimensional coordinates onto a 2D image plane.
The image plane is parallel to the first two basis vectors, with the third
basis vector defining the line of sight for depth calculations.

Key Components:
- Drawable: Abstract base class for renderable objects
- RenderContext: Provides rendering utilities and dependencies
- DrawableCave: Renders cave objects with hazard indicators
- DrawablePlayer: Renders the player with proper depth sorting

The depth sorting ensures that objects farther along the third basis (line of sight)
are drawn first, so closer objects appear on top, creating proper visual depth.
"""

import numpy.typing as npt
import pygame as pg
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .renderer import Renderer
    from wumpus.level import Level


class RenderContext:
    """Provides rendering utilities and dependencies to Drawable objects."""

    def __init__(self, renderer: 'Renderer', level: 'Level'):
        self.renderer = renderer
        self.level = level

    def get_rotated_coords(self, coords: npt.NDArray) -> npt.NDArray:
        """Get coordinates rotated by the renderer's current rotation."""
        return self.renderer.rotated(coords)

    def perp_dist(self, coords: npt.NDArray) -> float:
        """Get perpendicular distance along the line of sight (third basis) for foreshortening."""
        return self.renderer.perp_dist(coords)

    def project(self, coords: npt.NDArray, surf: pg.Surface) -> pg.Vector2:
        """Project arbitrary-dimensional coordinates to 2D screen space."""
        return self.renderer.project(coords, surf)

    def apply_depth_fade(self, color, coords: npt.NDArray) -> pg.Color:
        """Apply depth-based color fading along the line of sight."""
        return self.renderer.apply_depth_fade(color, coords)

    def draw_icon(self, surf: pg.Surface, icon: pg.Surface, size: int, opacity: int, center: pg.Vector2):
        """Draw an icon with scaling and opacity."""
        self.renderer.draw_icon(surf, icon, size, opacity, center)

    @property
    def pit_icon(self):
        return self.renderer.pit_icon

    @property
    def bat_icon(self):
        return self.renderer.bat_icon

    @property
    def wumpus_icon(self):
        return self.renderer.wumpus_icon

    @property
    def player_icon(self):
        return self.renderer.player_icon


class Drawable(ABC):
    """Abstract base class for objects that can be rendered."""

    @abstractmethod
    def get_coords(self) -> npt.NDArray:
        """Get the world coordinates of this drawable object."""
        pass

    @abstractmethod
    def paint(self, surf: pg.Surface, context: RenderContext):
        """Render this drawable object to the surface."""
        pass
