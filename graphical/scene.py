from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING, assert_never

if TYPE_CHECKING:
    from .transition import NewTransition, Transition

type SceneEvent = PushScene | PopScene | SwitchScene | NewTransition


@dataclass
class SwitchScene:
    scene: Scene


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

    def handle_pg_events(self) -> Iterator[SceneEvent]:
        yield from []

    def draw(self, surface, delta: float):
        ...


class SceneManager:
    """
    Switches between independent scenes. Each scene has its own render loop, handling pygame events.
    Only one scene is running at any given time. Scenes can be modal, stacking on top of eachother
    and resuming to previous scenes when done. Scenes communicate with the `SceneManager` by yielding
    `SceneEvent`s.
    """

    def __init__(self):
        self.scenes: list[Scene] = []
        self.transition: Transition | None = None

    def current(self) -> Scene | None:
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

    def handle_pg_events(self):
        """Passes pygame events to the current scene."""
        if self.transition is not None:
            return

        if not (current := self.current()):
            return

        from .transition import NewTransition, Transition

        for event in current.handle_pg_events():
            match event:
                case PopScene():
                    self.pop()
                case PushScene(scene):
                    self.push(scene)
                case SwitchScene(scene):
                    self.switch(scene)
                case NewTransition(new_scene, duration):
                    self.transition = Transition(
                        from_scene=self.current(),
                        to_scene=new_scene,
                        transition_duration=duration,
                    )
                    self.transition.enter()
                    self.switch(new_scene)
                case _:
                    assert_never(event)

    def draw(self, surface: pg.Surface, delta: float):
        """Draws the current scene."""
        if self.transition is not None:
            self.transition.draw(surface, delta)
            if not self.transition.is_blocking():
                self.transition = None
        elif scene := self.current():
            scene.draw(surface, delta)
