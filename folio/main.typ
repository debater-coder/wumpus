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
= Evaluation
== Implementation of Object Oriented Programming concepts
== Functionality
== Originality
== Documentation

#import "@preview/numbly:0.1.0": numbly
#counter(heading).update(0)
#set heading(numbering: numbly(
  "Appendix {1:A}.", // use {level:format} to specify the format
  "{1:A}.{2}.",
))

= Code structure
= Arbitrary Dimension Perspective Projection and Rotation
