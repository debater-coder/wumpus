from pygame.math import Vector2
from .drawable import Drawable, RenderContext
from dataclasses import dataclass
from wumpus import Cave
from wumpus.hazards import BottomlessPit, Superbats, Wumpus
from graphical.colours import COLOURS
import numpy as np
import pygame as pg

__all__ = ["DrawableCave", "DrawablePlayer"]


@dataclass
class DrawableCave(Drawable):
    cave: Cave
    explored: bool = True
    near_wumpus: bool = False
    is_hovered: bool = False
    is_in_shooting_path: bool = False
    show_wumpus: bool = False

    def get_coords(self) -> np.ndarray:
        return np.array(self.cave.coords)

    def paint(self, surf: pg.Surface, context: RenderContext, offsetx: float):
        coords = context.get_rotated_coords(self.get_coords())

        # Skip caves that are behind the camera
        if context.perp_dist(coords) <= 0:
            return

        center = context.project(coords, surf) + Vector2(offsetx, 0)
        radius = 100 / context.perp_dist(coords)

        if self.is_hovered:
            pg.draw.circle(
                surf,
                context.apply_depth_fade(COLOURS["yellow_500"], coords),
                center,
                radius + 20,
            )

        if self.is_in_shooting_path:
            pg.draw.circle(
                surf,
                context.apply_depth_fade(COLOURS["red_500"], coords),
                center,
                radius + 15,
            )

        hazard_in_cave = context.level.get_hazard_in_cave(self.cave)
        nearby_hazards = context.level.get_nearby_hazards(self.cave)
        has_nearby_pit = any(
            isinstance(hazard, BottomlessPit) for hazard in nearby_hazards
        )
        has_nearby_bats = any(
            isinstance(hazard, Superbats) for hazard in nearby_hazards
        )

        outline_layers = []

        if not hazard_in_cave and self.explored:
            if has_nearby_pit:
                outline_layers.append((COLOURS["green_500"], radius + 10))

            if has_nearby_bats:
                outline_layers.append((COLOURS["blue_500"], radius + 5))

        if not outline_layers:
            outline_layers.append((COLOURS["zinc_600"], radius + 5))

        # Proximity border
        for color, layer_radius in outline_layers:
            tinted_color = context.apply_depth_fade(color, coords)
            pg.draw.circle(surf, tinted_color, center, layer_radius)

        if self.explored:
            interior_color = COLOURS["zinc_950"]
        else:
            interior_color = COLOURS["zinc_600"]

        # Draw main cave circle
        tinted_interior = context.apply_depth_fade(interior_color, coords)
        pg.draw.circle(surf, tinted_interior, center, radius)

        # Wumpus indicator
        if self.near_wumpus:
            wumpus_radius = radius * 2 / 3
            tinted_orange = context.apply_depth_fade(COLOURS["orange_500"], coords)
            pg.draw.circle(surf, tinted_orange, center, wumpus_radius)

        hazard_icon = None
        if self.explored:
            match hazard_in_cave:
                case BottomlessPit():
                    hazard_icon = context.pit_icon
                case Superbats():
                    hazard_icon = context.bat_icon
                case Wumpus() if self.show_wumpus:
                    hazard_icon = context.wumpus_icon

        if hazard_icon:
            context.draw_icon(
                surf,
                hazard_icon,
                int(radius),
                int(255 - 255 * max(0, min(0.5, coords[2]))),
                center,
            )


@dataclass
class DrawablePlayer(Drawable):
    cave: Cave

    def get_coords(self) -> np.ndarray:
        return np.array(self.cave.coords)

    def paint(self, surf: pg.Surface, context: RenderContext, offsetx: float):
        coords = context.get_rotated_coords(self.get_coords())

        # Skip if behind camera
        if context.perp_dist(coords) <= 0:
            return

        center = context.project(coords, surf) + Vector2(offsetx, 0)
        size = int(160 / context.perp_dist(coords))
        opacity = int(255 - 255 * max(0, min(0.5, coords[2])))

        if context.player_icon:
            context.draw_icon(surf, context.player_icon, size, opacity, center)
