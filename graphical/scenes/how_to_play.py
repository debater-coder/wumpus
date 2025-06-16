import pygame as pg

from ..scene import PopScene, Scene
from ..gui.button import Button
from ..colours import COLOURS


class HowToPlay(Scene):
    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen
        font = pg.font.Font(None, 64)

        self.back = Button(pg.Rect(40, 40, 300, 80), "Back", font)

        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill(COLOURS["stone_900"])

    def handle_pg_events(self, events: list[pg.event.Event]):
        self.screen.blit(self.background, (0, 0))
        if self.back.update():
            yield PopScene()

        self.back.paint(self.screen)
        pg.display.flip()
