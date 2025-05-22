PlayerController (Invokes level.handle_events(). Yields indicates events that need to be handled by PlayerController.)

    |
    v

Level (Handles events and passes on to Hazards)
    |
    v

Hazards (Emit events through iterator)
