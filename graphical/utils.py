import pygame as pg


def button_up():
    return any(
        map(
            lambda event: event.button == 1,
            pg.event.get(eventtype=pg.MOUSEBUTTONDOWN),
        )
    )
