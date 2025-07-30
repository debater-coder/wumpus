from collections.abc import Iterator
import pygame as pg

from graphical.progress import LevelScore, Progress
from graphical.scene import Scene, SceneEvent, SwitchScene
from graphical.scenes.playing.renderer import Renderer

from ..gui import Button, VStack
from ..utils import button_up
from ..colours import COLOURS


class Win(Scene):
    def __init__(
        self,
        screen: pg.surface.Surface,
        renderer: Renderer,
        level: int,
        score: LevelScore,
    ):
        self.screen = screen
        self.renderer = renderer
        self.level = level
        self.score = score

        self.clock = pg.time.Clock()
        font = pg.font.Font(None, 64)

        high_score = Progress().get_high_score(self.level, score) or score

        self.your_score = font.render(
            f"Your score: Deaths: {score.deaths} Time: {score.time:.2f}s",
            False,
            COLOURS["zinc_50"],
        )
        self.high_score = font.render(
            f"High score: Deaths: {high_score.deaths} Time: {high_score.time:.2f}s",
            False,
            COLOURS["zinc_50"],
        )

        self.buttons = ([
            Button(pg.Rect(0, 0, 0, 80), "Next level", font),
        ] if level < 4 else []) + [
            Button(pg.Rect(0, 0, 0, 80), "Replay level", font),
            Button(pg.Rect(0, 0, 0, 80), "Exit to Main Menu", font),
        ]
        self.stack = VStack(self.buttons, width=600, gap=20)

        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill(COLOURS["zinc_950"])

    def update(self) -> Iterator[SceneEvent]:
        self.stack.rect.left = self.screen.get_rect().left + 40
        self.stack.rect.centery = self.screen.get_rect().centery
        self.stack.update()
        up = button_up()

        next_level, replay, exit = [button.update(up) for button in self.buttons]

        if next_level:
            from graphical.scenes.playing import Playing

            yield SwitchScene(Playing(self.screen, self.level + 1))

        if replay:
            from graphical.scenes.playing import Playing

            yield SwitchScene(Playing(self.screen, self.level))

        if exit:
            from graphical.scenes.menu import MainMenu

            yield SwitchScene(MainMenu(self.screen))

    def paint(self):
        delta = self.clock.tick(60)
        self.screen.blit(self.background, (0, 0))

        self.renderer.rotate(
            self.renderer.basis_vectors[2][1] ^ self.renderer.basis_vectors[0][1],
            delta / 20000,
        )
        if len(self.renderer.basis_vectors) > 3:
            self.renderer.rotate(
                self.renderer.basis_vectors[3][1] ^ self.renderer.basis_vectors[1][1],
                delta / 20000,
            )

        self.renderer.paint(
            self.screen,
            show_wumpus=True,
            explored=set(self.renderer.level.level.keys()),
            offsetx=200,
        )

        for button in self.buttons:
            button.paint(self.screen)

        self.screen.blit(self.your_score, (40, 40))
        self.screen.blit(self.high_score, (40, 120))
        pg.display.flip()

    def handle_pg_events(self):
        yield from self.update()
        self.paint()
