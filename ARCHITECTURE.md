# Hunt the Wumpus - Architecture Overview

## Event-Driven Architecture

This implementation uses an event-driven architecture to decouple game components and manage complex state interactions.

## Component Flow
```
TextPlayerController (User Interface)
    |
    | emits PlayerMoved, ArrowShot events
    v
PlayerController (Game Logic Coordinator)
    |
    | calls level.handle_event()
    v
Level (Central Event Dispatcher)
    |
    | dispatches to appropriate hazards
    | manages game state (player/hazard locations)
    v
Hazards (Game Entities)
    |
    | emit PlayerKilled, WumpusMoved, etc.
    | events bubble back up through Level
```

## Key Design Patterns

### Event-Driven Communication
- Components communicate through Events (dataclasses)
- Events flow through iterators using `yield` statements
- Prevents circular dependencies between Level and Hazards
- Enables complex event cascading (e.g., player enters cave → startles Wumpus → Wumpus moves → potentially kills player)

### Iterator-Based Event Handling
- Events are yielded through generator functions
- Allows for multiple events from single actions
- Enables event chaining and cascading effects
- Memory efficient for complex event sequences

### Hazard Strategy Pattern
- Each hazard type implements the same interface (`on_player_enter`, `on_arrow_enter`, etc.)
- Polymorphic behavior through method overriding
- Easy to add new hazard types

## Core Data Structures

### Cave System
- 20 interconnected caves forming a dodecahedron
- Each cave connects to exactly 3 others
- Defined in `level.json` with location and tunnel mappings

### Event Types
- **Movement Events**: `PlayerMoved`, `WumpusMoved`, `ArrowShot`
- **Game State Events**: `PlayerKilled`, `PlayerWon`, `ArrowHit`, `ArrowMissed`
- **Entity Events**: Base class `EntityMoved` for location changes

### Game State Distribution
- **Level**: Tracks hazard locations, cave structure, handles event routing
- **PlayerController**: Manages player location, game status (alive/win), user interface
- **Hazards**: Track their own locations, implement behavior logic

## Event Flow Examples

### Player Movement
1. User inputs move command
2. `TextPlayerController` calls `PlayerController.move()`
3. `PlayerController` emits `PlayerMoved` event to `Level`
4. `Level.handle_event()` updates player location
5. If hazard present, `Level` calls `hazard.on_player_enter()`
6. Hazard may emit `PlayerKilled`, which bubbles back to `PlayerController`

### Arrow Shooting
1. User inputs shoot command with room sequence
2. `PlayerController.shoot()` emits `ArrowShot` events for each room
3. `Level` checks for hazards in each room
4. If Wumpus hit, emits `ArrowHit` and `PlayerWon`
5. If no hits, emits `ArrowMissed`, triggering Wumpus startle behavior

## Benefits of This Architecture

1. **Decoupling**: Hazards don't need direct references to Level or Player
2. **Extensibility**: New hazard types easily added by implementing the interface
3. **Testability**: Components can be tested in isolation
4. **Complex State Management**: Event cascading handles intricate game interactions
5. **Memory Efficiency**: Iterator-based event handling avoids creating large event lists
