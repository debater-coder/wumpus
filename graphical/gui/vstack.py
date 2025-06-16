from typing import Sequence
import pygame as pg

from .element import Element


class VStack:
    """
    A vertical stack of elements.
    VStack only updates the `rect` property; updating and painting the elements is
    the responsibility of the caller.
    """

    def __init__(
        self,
        elements: Sequence[Element],
        width: int,
        pos: tuple[int, int] = (0, 0),
        gap: int = 0,
    ):
        self.elements = elements
        self.width = width
        self.gap = gap
        self.rect = pg.Rect(
            pos,
            (self.width, 0),
        )

    def update(self):
        self.rect = pg.Rect(
            self.rect.topleft,
            (
                self.width,
                sum(el.rect.height for el in self.elements)
                + self.gap * max(0, len(self.elements) - 1),
            ),
        )

        cumulative_height = self.rect.top
        for element in self.elements:
            rect = element.rect
            rect.top = cumulative_height
            rect.left = self.rect.left
            rect.width = self.width

            cumulative_height += rect.height + self.gap
