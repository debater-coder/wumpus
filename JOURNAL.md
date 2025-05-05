### 05/05/2025 git commit hash: `19c52af565583322ebfb73220f7fd8ead5119bbe`
#### Tasks completed
- Competed text based implementation of the game
- This implementation loads the game map from a JSON file
  - This is used to create the `Level` class, which holds the position of `Cave`s and `Hazard`s
  - `Hazard` has various subclasses for `Wumpus`, `BottomlessPit` and `Superbats`, which manipulate the `PlayerController` and `Level` on events such as `on_player_enter` (implemented as methods)
  - `PlayerController` has the actual player controlling functionality implemented in subclasses such as `TextPlayerController`
    - This will ease migration to a graphical implementation
#### Future improvements
- Add unit tests and documentation
- Change `Level` to an event-based system, where entities yield or return events that control the level, rather than having a tight coupling to the `Level` and `PlayerController`
