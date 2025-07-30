import pygame as pg

from dataclasses import dataclass

from ..colours import COLOURS
from .element import Element


@dataclass
class Button(Element):
    """A clickable GUI button element, with a label and changed colour on hover."""
    rect: pg.Rect
    text: str
    font: pg.font.Font

    hovered: bool = False
    bg_colour = COLOURS["zinc_900"]
    text_colour = COLOURS["zinc_50"]
    hover_colour = COLOURS["zinc_800"]

    def update(self, up: bool):
        self.hovered = self.rect.collidepoint(pg.mouse.get_pos())

        return self.hovered and up

    def paint(self, surface: pg.surface.Surface):
        background = self.hover_colour if self.hovered else self.bg_colour

        pg.draw.rect(surface, background, self.rect, border_radius=16)

        text_surf = self.font.render(
            self.text,
            True,
            self.text_colour,
        )

        text_pos = text_surf.get_rect(center=self.rect.center)

        surface.blit(text_surf, text_pos)
