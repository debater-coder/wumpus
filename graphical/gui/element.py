import pygame as pg
from dataclasses import dataclass


@dataclass
class Element:
    """The base class for elements that can be rendered in a stack."""
    rect: pg.Rect
