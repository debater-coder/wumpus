*The use of LLMs was allowed in this project.*

```
wumpus/
├── graphical/     # Graphical user interface: scenes, icons, GUI utilities
├── level_gen/     # Level generation logic and algorithms for different map types
├── text/          # Text-based interface and logic for terminal gameplay
└── wumpus/        # Core game logic: cave structure, events, hazards, player, levels
```

# Commands
## Running Unit Tests
```bash
python -m unittest
```

## Playing graphical
```bash
python -m graphical
```

## Playing text
```bash
python -m text
```

## Exporting folio to pdf
```bash
cd folio
typst compile main.typ
```
