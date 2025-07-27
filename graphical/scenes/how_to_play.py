import pygame as pg
import io
import importlib.resources

from ..utils import button_up

from ..scene import PopScene, Scene
from ..gui import Button
from ..colours import COLOURS


class HowToPlay(Scene):
    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen
        font = pg.font.Font(None, 64)

        self.back = Button(pg.Rect(10, 10, 300, 80), "Back", font)
        self.back.bg_colour = COLOURS["blue_900"]
        self.back.hover_colour = COLOURS["blue_800"]

        import graphical.scenes
        image_data = importlib.resources.read_binary(graphical.scenes, "how_to_play.png")
        self.image = pg.image.load(io.BytesIO(image_data)).convert()

    def handle_pg_events(self):
        self.screen.blit(self.image, (0, 0))
        if self.back.update(button_up()):
            yield PopScene()

        self.back.paint(self.screen)
        pg.display.flip()
