import pygame as pg
from .scene import SceneManager
from .scenes.menu import MainMenu

pg.init()
screen = pg.display.set_mode((1920, 1080), pg.SCALED)
pg.display.set_caption("Wumpus")

clock = pg.time.Clock()

scene_manager = SceneManager()
scene_manager.push(MainMenu(screen))

while True:
    clock.tick(60)

    if pg.event.peek(eventtype=pg.QUIT):
        break

    scene_manager.handle_pg_events(pg.event.get())


pg.quit()
