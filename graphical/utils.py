import pygame as pg


def button_up():
    return any(
        map(
            lambda event: event.button == 1,
            pg.event.get(eventtype=pg.MOUSEBUTTONDOWN),
        )
    )


def apply_opacity(color, opacity: float) -> pg.Color:
    """
    Apply opacity to a color, only affecting the alpha channel.
    
    Args:
        color: Base color (RGB tuple or pygame Color)
        opacity: Opacity value from 0.0 (transparent) to 1.0 (opaque)
        
    Returns:
        Color with specified opacity applied
        
    Examples:
        # Make a color 50% transparent
        semi_transparent = apply_opacity((255, 0, 0), 0.5)  # Red with 50% opacity
        
        # Make a color fully opaque
        opaque = apply_opacity((0, 255, 0), 1.0)  # Green with full opacity
        
        # Make a color nearly transparent
        faded = apply_opacity((0, 0, 255), 0.1)  # Blue with 10% opacity
    """
    result_color = pg.Color(color)
    result_color.a = int(255 * max(0.0, min(1.0, opacity)))
    return result_color



