## 05/05/2025 git commit hash: `19c52af565583322ebfb73220f7fd8ead5119bbe`
### Progress
- Competed text based implementation of the game
- This implementation loads the game map from a JSON file
  - This is used to create the `Level` class, which holds the position of `Cave`s and `Hazard`s
  - `Hazard` has various subclasses for `Wumpus`, `BottomlessPit` and `Superbats`, which manipulate the `PlayerController` and `Level` on events such as `on_player_enter` (implemented as methods)
  - `PlayerController` has the actual player controlling functionality implemented in subclasses such as `TextPlayerController`
    - This will ease migration to a graphical implementation
### Future improvements
- Add unit tests and documentation
- Change `Level` to an event-based system, where entities yield or return events that control the level, rather than having a tight coupling to the `Level` and `PlayerController`

## 22/05/2025 git commit hash `854cebf7a5eb777694642c36225013d7ddd866ef`
### Progress
- Added event based architecture
- This helped to decouple the Hazards from the Level
- Handling of player interaction with Hazards was also moved to Level.

## 13/06/2025 git commit hash `9003447fea0d29cc30092adac94c328893a5294f`
### Progress
- Complete migration to event based architecture
- Separate text-based game completely from core logic
- Add automated black-box testing
- Fix various edge cases (eg: shooting to room not adjacent to current room)
- Install pygame to nix shell
### Future tasks
- Create graphical package

## 20/05/2025 git commit hash `6a933ba5beb2a14ae5db1195709b73e29b06c576`
### Progress
- Created graphical package
  - Has a stack of scenes (Main Menu, Level Select, How to Play, Playing, Paused)
  - Modal scenes can be pushed onto stack and pop'ed to preserve game state
- Used force directed graph drawing to draw level onto scene
  - However, force directed graph drawing prefers to have all edges same length
  - So level map converges onto a perspective-like map with crossings, rather than a flattened map
### Future tasks
- I've decided against continuing with a flat 2D approach, rather using perspective projection of the actual polyhedral graph
- Hunt the Wumpus uses a dodechedral graph, so similar levels modelled after Platonic solids can be made

## 20/07/2025 git commit hash `106c2d65c672cbe5ac7d59964eb6f37db517d4f2`
### Progress
- Playable graphical version
  - Uses Renderer class to draw level, Caves and Player are Drawable instances that get sorted by depth
  - Arbitrary dimension perspective projection allows for 3D and 4D levels (or potentially higher in the future)
  - Created 4 levels (3 3D levels and 1 4D)
  - Animations when moving player or shooting to rotate view -- so the player doesn't constantly have to
  reposition the camera
  - Spinning level graphics on main menu
  - Death counter and screen tint to indicate player death
    - I do this since this game will take a few deaths to complete due to randomness
    - Deaths are a level statistic that players can try to optimise as a *high score*
### Future tasks
- Scene transitions
- How to play
- Credits menu
- Win screen (with high score)
- Level 5
- Level unlocking
- Sound effects

## 31/07/2025 git commit hash `0d256ab3988070b43b3bfdcdfaa36fc65c97d851`
### Progress
- How to play
- Win screen
- Level 5 completed
- Level unlocking

Due to time limitations I did not get to:
- Sound effects
- Credits menu (but I will include these in the folio)
