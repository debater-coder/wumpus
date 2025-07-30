import pygame as pg
import math
import importlib.resources
from typing import Optional


def button_up():
    """
    Returns whether the primary mouse button has been pressed then released.
    Used to detect button clicks.
    """
    return any(
        map(
            lambda event: event.button == 1,
            pg.event.get(eventtype=pg.MOUSEBUTTONUP),
        )
    )


def apply_fade(color, fade_factor: float) -> pg.Color:
    """
    Apply fading effect by lerping to black

    Args:
        color: Base color (RGB tuple or pygame Color)
        fade_factor: Fade value from 0.0 (black) to 1.0 (original color)

    Returns:
        Color lerped towards black based on fade factor

    Examples:
        # Make a color 50% faded
        semi_faded = apply_fade((255, 0, 0), 0.5)  # Red faded to darker red

        # Keep original color
        bright = apply_fade((0, 255, 0), 1.0)  # Green unchanged

        # Make a color very dark
        dark = apply_fade((0, 0, 255), 0.1)  # Blue nearly black
    """
    return pg.Color(color).lerp((0, 0, 0), 1.0 - max(0.0, min(1.0, fade_factor)))


def load_icon(package, filename: str) -> Optional[pg.Surface]:
    """
    Load an icon from a package using importlib.resources.

    Args:
        package: Package containing the icon (e.g., graphical.icons)
        filename: Icon filename (e.g., "wumpus.png")

    Returns:
        Loaded pygame Surface with alpha, or None if loading fails
    """
    try:
        icon_data = importlib.resources.read_binary(package, filename)
        import io

        icon_file = io.BytesIO(icon_data)
        return pg.image.load(icon_file).convert_alpha()
    except (FileNotFoundError, ModuleNotFoundError, AttributeError):
        return None


def recolor_icon(surface: pg.Surface, color) -> pg.Surface:
    """
    Recolor an icon to a specific color while preserving its shape.

    Args:
        surface: Original pygame Surface with alpha channel
        color: Target color (RGB tuple or pygame Color)

    Returns:
        New surface with the shape recolored to the specified color
    """
    # Use the original image's alpha channel to cut out the shape
    mask = pg.mask.from_surface(surface)
    mask_surface = mask.to_surface(setcolor=color, unsetcolor=(0, 0, 0, 0))
    return mask_surface


def load_and_recolor_icon(package, filename: str, color) -> Optional[pg.Surface]:
    """
    Load an icon and recolor it in one step.

    Args:
        package: Package containing the icon (e.g., graphical.icons)
        filename: Icon filename (e.g., "wumpus.png")
        color: Target color (RGB tuple or pygame Color)

    Returns:
        Loaded and recolored pygame Surface, or None if loading fails

    Examples:
        # Load and make wumpus red
        wumpus = load_and_recolor_icon(graphical.icons, "wumpus.png", COLOURS["red_400"])

        # Load and make bat blue
        bat = load_and_recolor_icon(graphical.icons, "bat.png", COLOURS["blue_400"])
    """
    original = load_icon(package, filename)
    if original:
        return recolor_icon(original, color)
    return None


def tween(t: float):
    """
    Returns a number between 0 and 1 based on a time value.
    Uses the ease-in-out-sinusoidal function to naturally
    transition between two values.
    """
    return -(math.cos(math.pi * t) - 1) / 2
