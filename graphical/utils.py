import pygame as pg


def button_up():
    return any(
        map(
            lambda event: event.button == 1,
            pg.event.get(eventtype=pg.MOUSEBUTTONDOWN),
        )
    )


def apply_fade(color, fade_factor: float) -> pg.Color:
    """
    Apply fading effect by lerping to black (since pg.draw doesn't support alpha).
    
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



