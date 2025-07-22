from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Literal, override

import pygame as pg

from .scene import Scene, SceneEvent
from .utils import animate, clamp

TransitionState = Literal["fade-in", "idle", "fade-out"]
TRANSITION_DURATION = 0.2  # seconds


@dataclass
class NewTransition:
    """Event to start a new transition."""

    new_scene: Scene
    duration: float = TRANSITION_DURATION


class Transition(Scene):
    """A scene that smoothly transitions from one scene to another."""

    def __init__(
        self,
        from_scene: Scene | None,
        to_scene: Scene,
        transition_duration: float = TRANSITION_DURATION,
    ):
        self.from_scene = from_scene
        self.to_scene = to_scene
        self.transition_duration = transition_duration

        self.from_surface = pg.Surface(pg.display.get_window_size())
        self.to_surface = pg.Surface(pg.display.get_window_size())

        self.state: TransitionState = "fade-out"
        self.progress = 0.0

    @override
    def enter(self):
        # Render what the last scene looked like
        if self.from_scene is not None:
            self.from_scene.draw(self.from_surface)

        # Let the new scene know that it's being entered
        self.to_scene.enter()
        self.to_scene.draw(self.to_surface)

    @override
    def handle_pg_events(self) -> Iterator[SceneEvent]:
        yield from []

    def draw(self, surface: pg.Surface, delta: float):
        """We manually draw the scenes to a buffer, and then fade between them."""
        # Update fade animation
        self.progress = clamp(self.progress + delta / self.transition_duration, 0, 1)

        if self.state == "fade-out":
            self.from_surface.set_alpha(animate(self.progress, 255, 0))
            surface.blit(self.from_surface, (0, 0))

            if self.progress == 1:
                self.state = "fade-in"
                self.progress = 0
        elif self.state == "fade-in":
            self.to_surface.set_alpha(animate(self.progress, 0, 255))
            surface.blit(self.to_surface, (0, 0))
        elif self.state == "idle":
            # We're done, let the scene manager know
            ...

    def is_blocking(self) -> bool:
        """If the transition is still ongoing."""
        return self.state != "idle"
