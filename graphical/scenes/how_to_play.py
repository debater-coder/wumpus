from typing import override
import pygame as pg

from ..utils import button_up

from ..scene import PopScene, Scene
from ..gui import Button
from ..colours import COLOURS


class HowToPlay(Scene):
    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen
        font = pg.font.Font(None, 64)

        self.back = Button(pg.Rect(40, 40, 300, 80), "Back", font)

        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill(COLOURS["zinc_950"])

    @override
    def handle_pg_events(self):
        if self.back.update(button_up()):
            yield PopScene()

    @override
    def draw(self, surface: pg.Surface, delta: float):
        surface.blit(self.background, (0, 0))
        self.back.paint(surface)
