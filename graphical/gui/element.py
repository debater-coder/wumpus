import pygame as pg
from dataclasses import dataclass


@dataclass
class Element:
    rect: pg.Rect
