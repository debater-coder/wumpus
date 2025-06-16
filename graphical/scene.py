from __future__ import annotations
from collections.abc import Iterator
from dataclasses import dataclass
from typing import assert_never

import pygame as pg

type SceneEvent = PushScene | PopScene | SwitchScene


@dataclass
class PushScene:
    scene: Scene


@dataclass
class PopScene:
    pass


@dataclass
class SwitchScene:
    scene: Scene


class Scene:
    def enter(self):
        pass

    def exit(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def handle_pg_events(self, events: list[pg.event.Event]) -> Iterator[SceneEvent]:
        yield from []


class SceneManager:
    """
    Switches between independent scenes. Each scene has its own render loop, handling pygame events.
    Only one scene is running at any given time. Scenes can be modal, stacking on top of eachother
    and resuming to previous scenes when done. Scenes communicate with the `SceneManager` by yielding
    `SceneEvent`s.
    """

    def __init__(self):
        self.scenes: list[Scene] = []

    def current(self):
        if len(self.scenes) > 0:
            return self.scenes[-1]
        return None

    def push(self, scene: Scene):
        """Enters into a new scene, temporarily pausing the last scene."""
        # pause last scene
        if current := self.current():
            current.pause()

        self.scenes.append(scene)
        scene.enter()  # enter new scene

    def pop(self):
        """Exits from the current scene, resuming the last scene."""
        self.scenes.pop().exit()  # exit last scene

        # resume new scene
        if current := self.current():
            current.resume()

    def switch(self, new_scene: Scene):
        """Exits all scenes, entering the specied scene"""
        for scene in self.scenes:
            scene.exit()

        self.scenes.clear()  # this preserves the reference of the current scene list
        self.push(new_scene)

    def handle_pg_events(self, events: list[pg.event.Event]):
        """Passes pygame events to the current scene."""
        if not (current := self.current()):
            return

        for event in current.handle_pg_events(events):
            match event:
                case PopScene():
                    self.pop()
                case PushScene(scene):
                    self.push(scene)
                case SwitchScene(scene):
                    self.switch(scene)
                case _:
                    assert_never(event)
