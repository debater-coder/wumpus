import pygame as pg

from ..scene import Scene


class LevelSelect(Scene):
    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen
