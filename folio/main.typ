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

#outline(depth: 1)
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
== Internal represenation
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

#table(
  columns: 4,
  [*Initial state*], [*User Action*], [*Expected Output*], [*Reason*],
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
== Functionality
- TODO: write about how tunnels always draw behind nodes and how that is technically wrong.
== Originality
== Documentation

#import "@preview/numbly:0.1.0": numbly
#counter(heading).update(0)
#set heading(numbering: numbly(
  "Appendix {1:A}.", // use {level:format} to specify the format
  "{1:A}.{2}.",
))

= Code structure
#cmarker.render(read("./README.md"), h1-level: 2)

= Arbitrary Dimension Perspective Projection and Rotation
