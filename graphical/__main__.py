import pygame as pg

from .colours import COLOURS

pg.init()
screen = pg.display.set_mode((1280, 720), pg.SCALED)
pg.display.set_caption("Wumpus")

background = pg.Surface(screen.get_size()).convert()
background.fill(COLOURS["stone_900"])

screen.blit(background, (0, 0))
pg.display.flip()

clock = pg.time.Clock()

running = True
while running:
    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

pg.quit()
