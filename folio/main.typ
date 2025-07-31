#set text(
  font: "Rubik",
)
#set heading(numbering: "1.")
#show link: underline
#set page(header: context [
  Software Engineering Preliminary HSC Course – Object-Oriented Programming #h(1fr) #counter(page).display("1")
], paper: "a3")
#align(center, text(17pt)[*Wumpus: Network \
Object Oriented Programming Assessment Task*])

#align(center)[Hamzah Ahmed]

#outline()
= Overview
This document provides documentation for the Preliminary Object Oriented Programming
Project. The appendixes provide external documentation and context useful for those
studying the code.

== Hunt the Wumpus: Background

*Hunt the Wumpus* is a classic computer game originally created in 1972 by Gregory
Yob. The game is set in a series of interconnected caves, where the player must
hunt a creature known as the Wumpus. The player navigates the cave system,
avoiding hazards such as bottomless pits and super bats, while attempting to
deduce the Wumpus's location and shoot it to win the game.

== Wumpus: Network
*Wumpus: Network* is the result of this project. It is a game inspired by Hunt
the Wumpus, adding original features. It is a graphical game with 3D and 4D
levels, expanding the scope of the original game with more challenging and
interesting levels.

= Journal
#import "@preview/cmarker:0.1.6"

#cmarker.render(read("./JOURNAL.md"))
= System Modelling
== Structure Charts
=== Wumpus
#image("Wumpus Structure-Wumpus.png")
=== Handle Playing
#image("Wumpus Structure-Handle Playing.png")
=== Handle Level Select
#image("Wumpus Structure-Handle Level Select.png")
== Class Diagram
#image("Class Diagram.png")
= Data Dictionary
== Internal representation
#let data_dictionary_table(text) = table(
  columns: (1fr, 1fr, 2fr, 1fr, 2fr),
  align: (auto, auto, auto, center, auto),
  [*Data Structure (type)*],[*Attributes*],[*Data type*],[*Max length*],[*Description*],
  ..csv(bytes(text)).flatten()
)

#data_dictionary_table("
PlayerController (object),alive,Boolean,1,Whether the player is alive
,cave,Cave object,EOF,Current cave the player is in
,initial_cave,Cave object,EOF,Cave where the player first spawned in (used for respawn)
,level,Level object,EOF,Level object containing caves and hazards
,win,Boolean,1,Whether the player has won
")

#data_dictionary_table("
Level (object),hazards,Array of hazard objects,EOF,The hazard objects in the level
,level,Hashmap of Integer to the Cave objects,EOF,Maps cave location number to cave objects
,player,Integer,3,Cave location number of the player
")

#data_dictionary_table("
Cave (object),location,Integer,3,This cave's location number
,tunnels,Array of integers,EOF,Array of cave location numbers this cave connects to
,coords,Array of reals,EOF,3D coordinates of cave
")
#data_dictionary_table("
Hazard (object),level,Hashmap of Integer to Cave object,EOF,Maps cave location number to cave objects
,location,Integer,3,Hazard's location number
")
== Graphical
#data_dictionary_table("
SceneManager (object),scenes,Array of Scene objects,EOF,A stack where the top scene is the one that is shown
")
#data_dictionary_table("
MainMenu (Scene),buttons,Array of Button objects,EOF,Buttons that are shown on screen
")
#data_dictionary_table("
HowToPlay (Scene),back,Button object,EOF,Button to close the menu
")
#data_dictionary_table("
LevelSelect (Scene),buttons,Array of Button objects,EOF,Buttons to enter each menu
,back,Button object,EOF,Button to return to main menu
")
#data_dictionary_table("
Playing (Scene),level,Level object,EOF,Level object containing caves and hazards (see above)
,player,PlayerController object,EOF,PlayerController to control actions of player (see above)
")
#data_dictionary_table("
DeathMenu (Scene),buttons,Array of Button objects,EOF,Buttons that are shown on screen
")
#data_dictionary_table("
WinMenu (Scene),buttons,Array of Button objects,EOF,Buttons that are shown on screen
")
#data_dictionary_table("
Button (Scene),bg_colour,RGB colour,6,Background colour of button
,font,Font file,EOF,Font file to text
,hover_colour,RGB colour,6,Background colour of button when hovered
,hovered,Boolean,1,Whether the button is currently hovered
,rect,Array of integers,4,\"Top, left, width, height coordinates of button\"
,text,String,100,Label to show on the button
,text_colour,RGB colour,6,Colour to draw the text
")
= Testing Strategies
== Main Game
#set table.cell(breakable: false)
#table(
  columns: (2fr, 1fr, 2fr, 1fr),
  table.header(repeat: true, [*Initial state*], [*User Action*], [*Expected Output*], [*Reason*]),
  [
#image("screenshots/image.png")
], [Click and drag], [
#image("screenshots/image (1).png")
], [Test rotating view],
  [
#image("screenshots/image (2).png")
], [Scroll down], [
#image("screenshots/image (3).png")
], [Test zooming in],
  [
#image("screenshots/image (2).png")
  ], [Scroll up], [
#image("screenshots/image (5).png")
], [Test zooming out],
  [
#image("screenshots/image (6).png")
], [Left-click on cave adjacent to player], [
#image("screenshots/image (7).png")
], [Clicking on a cave should cause the player to move to it],
  [#image("screenshots/image (7).png")], [Left-click on cave not adjacent to player], [_no change_], [Player can only move to an adjacent cave],
  [#image("screenshots/image (7).png")], [Right-click on cave not adjacent to player], [_no change_], [Arrows cannot skip caves],
  [
#image("screenshots/image (7).png")
], [Right-click on a cave adjacent to player], [#image("screenshots/image (8).png")], [Right-clicking specifies a shooting path (highlighted in red)],
[#image("screenshots/image (8).png")], [Right-click on a cave not adjacent to end of shooting path], [
  #image("screenshots/image (9).png") _Shooting path has been reset_
], [Arrows cannot skip caves],
  [#image("screenshots/image (10).png")
    _Notice the shooting path contains exactly 5 caves_], [Right click on any cave], [#image("screenshots/image (10).png")
_no change_
], [Arrows can travel a maximum of 5 caves],
  [#image("screenshots/image (10).png")], [Press the 'c' key], [
    #image("screenshots/image (11).png")
], [Pressing the 'c' key after  selecting a shooting path will reset it.],
  [#image("screenshots/image (12).png")
 _Notice that the player's cave is highlighted as part of the shooting path_], [Shoot cave player is in (by pressing enter)], [#image("screenshots/image (13).png")], [Shooting oneself leads to death and immediate respawning],
  [#image("screenshots/image (14).png")], [Shoot cave Wumpus is in], [#image("screenshots/image (15).png")], [Shooting the Wumpus completes the level],
  [#image("screenshots/image (16).png")], [Moving into cave with pit], [#image("screenshots/image (17).png")], [Pit leads to death and immediae respawning],
  [#image("screenshots/image (18).png")], [Moving into cave with bat], [#image("screenshots/image (19).png")], [Bats teleport player to random cave],
)

= Evaluation
== Implementation of Object Oriented Programming concepts
=== Encapsulation
Encapsulation is the bundling of attributes with methods to hide internal details about an object
that other modules are not concerned with. An example of this is the *Facade pattern*.

The core Wumpus game logic is separated from the graphical package, as the graphical code
is not concerned with it. Thus, I use the Facade pattern in `PlayerController` to provide
a simplified external interface to the game logic.

```py

class PlayerController:
    """
    Responsibility:
        - Emit events to level like PlayerMoved
        - Handle events such as PlayerKilled
    """

    def __init__(self, level: Level):
        self.level = level

        self.cave = level.choose_empty_cave()
        self.initial_cave = self.cave
        self.alive = True
        self.win = False

        list(self.emit_to_level(PlayerMoved(self.cave.location)))

    def move(self, location: int):
        list(self.emit_to_level(PlayerMoved(location)))

    def shoot(self, locations: list[int]):
        for location in locations:
            if any(
                [
                    isinstance(event, ArrowHit)
                    for event in self.emit_to_level(ArrowShot(location))
                ]
            ):
                return

        self.emit_to_level(ArrowMissed())

    def emit_to_level(self, event: Event) -> Iterator[ArrowHit]:
        ... # omitted for brevity

    def handle_msg(self, msg: str):
        pass

    def get_nearby_msgs(self):
        ... # omitted for brevity

    def respawn(self):
        ... # omitted for brevity
```

This class is an example of the Facade pattern, as the internal details of the event system is
hidden from the other modules which use this class. Instead, other modules call the `PlayerController`'s
methods to perform actions on the player. For example:
```py
player.move(7)
if not player.alive:
    player.respawn()
```
=== Inheritance
Inheritance allows for a child class to reuse the methods and attributes of its parent class,
while only overriding behaviour that differs. Inheritance is used as a mechanism for code reuse
in the inheritance between `TextPlayerController` and `PlayerController`.


```py
class TextPlayerController(PlayerController):
    def play(self) -> bool:
        """Play the game, returns whether the game was won or lost."""
        while self.alive and not self.win:
            self.get_action()
        return self.win

    def get_action(self):
        ... # text handling omitted for brevity

    def handle_msg(self, msg: str):
        print(msg)
```

This class demonstrates reuse of the core game logic defined in `PlayerController`, while
adding additional functionality allowing it to be controlled using text.
==== Polymorphism
Inheritance is also used to achieve dynamic polymorphism, allowing multiple classes to share
a common interface to implement different behaviours. This can be seen in the `Hazard` class and
its subclasses.

```py
class Hazard:
    """
    Hazards are located in a cave, they can affect the player's location or
    cause the player to lose.
    """

    def __init__(self, level: dict[int, Cave]):
        self.location: int | None = None
        self.level = level

    def on_arrow_miss(self) -> Iterator[Event]:
        """Called when an arrow does not hit any hazards that are not immune."""
        yield from []

    def on_arrow_enter(self) -> Iterator[Event]:
        """
        Called when an arrow hits the cave this hazard is in.

        Returns: Whether the arrow has considered to 'hit' the hazard.
        Most hazards are immune by arrows, so they should return False.
        """
        yield from []

    def on_player_enter(self) -> Iterator[Event]:
        """Called when the player enters the cave this hazard is in."""
        yield from []

    def nearby_msg(self) -> str:
        """Returns a message to be printed when a hazard is nearby."""
        return "Unknown hazard nearby."

class BottomlessPit(Hazard):
    """Kills the player when it enters the cave."""

    def nearby_msg(self):
        return "I feel a draft."

    def on_player_enter(self):
        yield "You fell into a bottomless pit."
        yield PlayerKilled()
```

Here, the `Hazard` parent class defines a common interface for hazards to define their interactions.
It contains blank implementations of hazard reactions to different events. Thus, as seen in
`BottomlessPit`, child classes only need to override functionality that they actually implement,
while still allowing all hazards to be controlled in a unified way. This is considered polymorphism
(meaning "many forms"), as objects of different classes can be used in the same way, without being
concerned with what specific subclass is in use.
=== Evaluation of implementation of OOP concepts
This project demonstrates a strong implementation of OOP concepts, effectively using classes and
methods to reuse functionality.
== Functionality
#grid(columns: 2, gutter: 2pt, image("screenshots/evaluation/how_to_play.png"),
image("screenshots/evaluation/level_select.png"),
image("screenshots/evaluation/main_menu.png"),
image("screenshots/evaluation/paused.png"),
image("screenshots/evaluation/win.png"))
=== Features
This project provides a complete, playable game with 5 different levels. Each level provides a unique
map with randomly spawned hazards which can be interacted with. The game features menus including:
- Main Menu
- Level Select
- How to Play
- Pause Menu
- Win Menu

This game has a progress mechanism where levels are "locked", until the level before it has been completed.
This allows for a gradual increase in difficulty as the player completes the game. Futhermore, this game
has a high score mechanism, which keeps track of the number of times the player has died in the level
and how long the player takes to complete.

Within a level, my game implements features close to the original Hunt the Wumpus game. It includes the three
original hazards: Wumpus, Bottomless Pit, Superbats and similar movement and shooting mechanics to the original
game. Added functionality includes the ability to rotate the 3D view and zoom in and out (further explained in @perspective).

=== Polish
Polish refers to features which improve the player experience with subtle tweaks and refinements.
Some examples of polish in this game:
- Camera rotation animation when clicking on a cave
- Brief red tint on screen which fades out to give an indication of player death
- Animations follow a more realistic easing curve -- animations don't abruptly start and stop rather they speed up and slow down similar to real world objects
- When the mouse cursor is "hovered" over a clickable button, it changes colour subtly to indicate that it is clickable
- Borders on buttons are slightly rounded
- Important buttons like the pause button, back button or the next unplayed level in level select are a different colour for visual contrast to draw attention to them
- The Main Menu features a rotating Wumpus cave in the background for visual interest
- Upon completing a level, the entire shape of the level is revealed in a slowly rotating view
=== Possible improvements
There are some small features that could further improve player experience, but have not been implemented due to time:
- Sound effects
- Fade transitions between screens
- A settings menu to reset progress
- Text on screen to supplement visual indication of hazards
- Further levels could introduce novel hazards
- Credits in an in-game menu (see @credits)

There is also a visual inconsistency in the way tunnels are rendered. The lines that represent tunnels
will always render behind all caves, however sometimes this is incorrect. This is rarely noticable
but fixing this could improve player experience.

=== Evaluation of functionality
This is a complete and functional game, with a high degree of polish and additional features. While it does
lack some features that would be recommended for a public release of a game, it is certainly in a *playable state*
with multiple levels and menus.
== Originality
This project provides an original interpretation of the Hunt the Wumpus game
while staying true to the original intentions of the game. The original game was
text-based, containing a single level. Hunt the Wumpus was created due to the
*creator's frustrations with the multitude of "hide and seek computer game[s]"
based on square grids*. Yob's innovation was creating a hide and seek game where
the caves were a *non-grid pattern*. However, *graphical versions of the game
present their levels on a square grid*, usually by *"flattening"* the caves
network by forcing them to fit on a square grid. *This ultimately limits the
complexity of levels in these games to those that fit on a grid.*

This game provides a different interpretation, *preserving the non-grid pattern
of the original game*. It does this through arbitrary dimension perspective
projection and rotation (described in @perspective). What this means is the game
rendering logic can draw levels of any dimension greater than or equal to 3. To
effectively explore these levels, this game provides *zoom and rotate
functionality*. *There are 3 3D levels and 2 2D levels included*. The mechanisms and intuition
for understanding higher dimensions than 3 are provided in @perspective, but
they are not necessary to be able to play the levels. The purpose of these
levels is to present a *further challenge to the player* that would not be common
in other video games.

=== Levels
All levels have cave structures based on different mathematically interesting shapes.

/ Level 1: Dodecahedron (3D) _This level was also used in the original textual *Hunt the Wumpus*, but here it is playable in 3D._
/ Level 2: Icoasahedron (3D)
/ Level 3: Mobius strip (3D)
/ Level 4: Tesseract (4D)
/ Level 5: 24-cell (4D)

=== Evaluation of originality
*Wumpus: Network* is a highly original interpretation of *Hunt the Wumpus*,
providing unique features that are rare even for video games in general. It does
this while preserving the experience of playing the original game, by keeping
the same core mechanic of deducing where hazards are based on the current cave.
While my game does not add new hazards or interactions compared to the original
version, it instead explores how this could be extended in more complex and
challenging levels, as well as a novel interface.

This project implements a feature set significantly different provided in the
support resource. Even without the graphical implementation, *this project
implements key features of the textual Hunt the Wumpus not present in the guided
walkthrough*, such as the ability for the Wumpus to move between caves, and
randomly spawned hazards.

== Documentation
This project has both internal and intrinsic documentation within the codebase.
=== Intrinsic
Intrinisic documentation makes the code more understandable by using clear
structure and naming within the structures of the code itself.

*Examples:*
```py
@dataclass
class Cave:
    location: int
    tunnels: list[int]
    coords: tuple[float, ...]
```
The class, attributes and type annotations within this code make the purpose and structure of the code clear.

```py
class Superbats(Hazard):
    def nearby_msg(self):
        return "Bats nearby."

    def on_player_enter(self):
        yield "ZAP -- Super bat snatch! Elsewhereville for you!"
        yield PlayerMoved(choice(list(self.level.values())).location)
```
The class and method names in this code make it clear what each hazard does.

```py
class PlayerController:
    def __init__(self, level: Level):
        self.level = level
        self.cave = level.choose_empty_cave()
        self.initial_cave = self.cave
        self.alive = True
        self.win = False
```

The names of the attributes in this class make the player's initial state clear.
The ```py level.choose_empty_cave()``` method has a descriptive name to help
readers of the code understand its purpose.

=== Internal
The need for internal documentation is reduced through intrinsic documentation, however
it is still important to describe the purpose of code, or to clarify complex procedures.

In Python, internal documentation takes the form of "docstrings" (special
comments tied to a specific method, function, class or module) or inline
comments.

*Examples:*

```py
class PlayerController:
    """
    Responsibility:
        - Emit events to level like PlayerMoved
        - Handle events such as PlayerKilled
    """
    ...
```
This class-level docstring explains the overall responsibility of the `PlayerController` class, making its role in the system clear.

```py
class Hazard:
    """
    Hazards are located in a cave, they can affect the player's location or
    cause the player to lose.
    """
    ...
    def on_player_enter(self) -> Iterator[Event]:
        """Called when the player enters the cave this hazard is in."""
        yield from []
```
Here, both the class and method docstrings describe the purpose and expected behavior, clarifying how hazards interact with the player.

```py
def emit_to_level(self, event: Event) -> Iterator[ArrowHit]:
    # This method sends an event to the level and yields any ArrowHit events in response.
    ...
```
This inline comment explains a non-obvious implementation detail about how events are handled and what is yielded.

```py
def on_arrow_enter(self) -> Iterator[Event]:
    """
    Called when an arrow hits the cave this hazard is in.

    Should yield an ArrowHit event if the arrow has considered to 'hit` the hazard.
    Most hazards are immune by arrows, so they should not yield this event.
    """
    yield from []
```
This method-level docstring provides additional context about the method's
purpose and its expected return value, especially clarifying the default
behavior for most hazards.

```py
class BottomlessPit(Hazard):
    """Kills the player when it enters the cave."""
    ...
```
A concise class docstring here makes the effect of the `BottomlessPit` hazard immediately clear to readers.
```py
"""
Events are used to decouple the Hazards from the Level.
Instead of directly invoking methods on Level, Hazards yield Events, which
are dispatched to Level. This also prevents circular type imports between Level
and Hazards.
"""
```
This module level docstring, makes it clear the overall purpose of this section
of code before readers go into specific classes or methods.

== Evaluation of documentation
This project is thoroughly documented with both internal and intrinsic documentation.

#import "@preview/numbly:0.1.0": numbly
#counter(heading).update(0)
#set heading(numbering: numbly(
  "Appendix {1:A}.", // use {level:format} to specify the format
  "{1:A}.{2}.",
), supplement: [])

= Code structure
#cmarker.render(read("./README.md"), h1-level: 2)

= Arbitrary Dimension Perspective Projection and Rotation <perspective>
== Perspective Projection
In this project, the game world is not restricted to the familiar two or three
dimensions, but can exist in any number of spatial dimensions. Each point within
the world is described by a list of real numbers. For example, a point in
four-dimensional space is represented as (x, y, z, w), where each coordinate is
a real number indicating position along that axis.

To render such a world on a two-dimensional screen, the system employs a process
called perspective projection. The first two coordinates (typically x and y) are
selected to define the image plane. The image plane is the flat surface onto
which the world is projected, corresponding to the screen itself. The third
coordinate (such as z in 3D) is treated as the depth direction, representing the
line of sight into the scene. In higher dimensions, the choice of which
coordinate acts as depth can be adjusted, allowing the player to explore and
visualize the extra dimensions by rotating the view.

Each point, defined by its real-number coordinates, is mathematically mapped
onto the image plane. The further a point lies along the depth direction, the
smaller and dimmer it appears, creating a convincing sense of perspective. This
mimics the way distant objects appear in real life, even when those objects
exist in dimensions beyond our direct experience.

== Rotation
Rotation is achieved using a field of mathematics called Geometric Algebra (also
known as Clifford Algebra, or shortened as GA). While a full description of the
field is out of scope, a brief relevant overview is provided below.

In this field, vectors (visualised as oriented line segments) are generalised to
bivectors (visualised as oriented areas), trivectors (visualised as oriented
volumes) and in general a $k$-grade element is a $k$-vector. In GA, we operate
on objects called multivectors, which are the linear combination of different
grade elements. For example 3D multivectors are $"scalar" + "vector" +
"bivector" + "trivector"$, and this generalises to arbitrary dimensions.

In 3D we often think about rotations as occurring around an axis, however
generally this is nonsensical. Consider that in 2D there is no orthogonal
axis for the rotation to occur "around", and in 4D there is more than one
unique direction perpendicular to any given plane! Thus, it is more
correct to treat rotations as occurring _in_ a plane. To represent this,
we use bivectors which are our 2 dimensional elements in the sum
that constitutes multivectors.

Thus we see rotation as an operation involving *a plane and an angle*.
It is trivial to obtain a bivector between any two arbitrary vectors,
so this is very useful for animating the camera rotation between two
caves.

Geometric algebra is extremely powerful, as it allows for concepts such
as arbitrary dimension rotation to be expressed very concisely. Below
are the equations used in this project. An explanation of these is out
of scope but a reference is provided in @credits

*Rotate vector by rotor:*
$ v' = R v R^(-1) $
where $v'$ is the rotated vector, $v$ is the initial vector and $R$ is the rotor.
This takes a vector and rotates it by the current rotor (which is initialised to the
scalar $1$).

*Update rotor by bivector and angle:*
$ R' = e^(B theta / 2) R $
where $R'$ is the updated rotor, $B$ is the bivector defining the plane of rotation, $theta$ is
the angle to rotate in radians and $R$ is the initial rotor. This equation will take
the current rotor (representing the current view angle) and rotate it by a plane and an angle.
Notice the $theta / 2$, is because this rotor will be applied twice
(multivectors are non-commutative). You may also notice that this looks simiar to rotation of
complex numbers in 2D or almost identical to rotation of
quaternions in 3D. This is because GA provides a generalisation that is isomorphic to these
constructs in lower dimensions.

= Credits <credits>
#cmarker.render(read("./CREDITS.md"), h1-level: 2)
