from typing import Union, Callable, Optional, Sequence
import typing
from .utils import tween


class Animator:
    """
    A class for animating values over time using smooth easing transitions.

    Uses the tween function from utils.py to provide natural ease-in-out-sinusoidal
    interpolation between start and end values.
    """

    def __init__(
        self,
        start_value: Union[float, int, Sequence[Union[float, int]]],
        end_value: Union[float, int, Sequence[Union[float, int]]],
        duration: float,
        on_complete: Optional[Callable[[], None]] = None,
    ):
        """
        Initialize the animator.

        Args:
            start_value: The initial value to animate from
            end_value: The target value to animate to
            duration: Animation duration in seconds
            on_complete: Optional callback function called when animation completes
        """
        if duration <= 0:
            raise ValueError("Duration must be positive")

        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.on_complete = on_complete

        # Animation state
        self.current_time = 0.0
        self.is_active = False
        self.has_completed = False

        # Validate that start and end values are compatible
        self._validate_values()

    def _validate_values(self):
        """Ensure start and end values are compatible types."""
        start_type = type(self.start_value)
        end_type = type(self.end_value)

        # Check if both are sequences
        if hasattr(self.start_value, "__len__") and hasattr(self.end_value, "__len__"):
            if len(typing.cast(Sequence, self.start_value)) != len(
                typing.cast(Sequence, self.end_value)
            ):
                raise ValueError("Start and end sequences must have the same length")
        elif start_type != end_type:
            # Allow int/float mixing
            if not (
                isinstance(self.start_value, (int, float))
                and isinstance(self.end_value, (int, float))
            ):
                raise ValueError("Start and end values must be compatible types")

    def start(self):
        """Start or restart the animation."""
        self.current_time = 0.0
        self.is_active = True
        self.has_completed = False

    def update(self, delta_time: float):
        """
        Update the animation by the given time step.

        Args:
            delta_time: Time elapsed since last update in seconds
        """
        if not self.is_active or self.has_completed:
            return

        self.current_time += delta_time

        if self.current_time >= self.duration:
            self.current_time = self.duration
            self.is_active = False
            self.has_completed = True

            # Call completion callback if provided
            if self.on_complete:
                self.on_complete()

    def get_value(self) -> Union[float, int, Sequence[Union[float, int]]]:
        """
        Get the current interpolated value.

        Returns:
            The current value based on animation progress
        """
        if self.current_time <= 0:
            return self.start_value
        if self.current_time >= self.duration:
            return self.end_value

        # Calculate progress (0 to 1)
        progress = self.current_time / self.duration

        # Apply easing using tween function
        eased_progress = tween(progress)

        return self._interpolate(self.start_value, self.end_value, eased_progress)

    def _interpolate(self, start, end, t: float):
        """
        Interpolate between start and end values using factor t.

        Args:
            start: Start value
            end: End value
            t: Interpolation factor (0 to 1)
        """
        # Handle sequences (tuples, lists)
        if hasattr(start, "__len__") and hasattr(end, "__len__"):
            result = []
            for s, e in zip(start, end):
                result.append(s + (e - s) * t)
            return type(start)(result)  # Return same type as input

        # Handle scalar values
        return start + (end - start) * t

    def is_finished(self) -> bool:
        """Check if the animation has completed."""
        return self.has_completed

    def reset(self):
        """Reset the animation to its initial state."""
        self.current_time = 0.0
        self.is_active = False
        self.has_completed = False

    def get_progress(self) -> float:
        """
        Get the current progress as a value between 0 and 1.

        Returns:
            Animation progress (0.0 = start, 1.0 = complete)
        """
        if self.duration == 0:
            return 1.0
        return min(self.current_time / self.duration, 1.0)

    def set_duration(self, new_duration: float):
        """
        Change the animation duration while preserving current progress.

        Args:
            new_duration: New duration in seconds
        """
        if new_duration <= 0:
            raise ValueError("Duration must be positive")

        # Preserve current progress
        current_progress = self.get_progress()
        self.duration = new_duration
        self.current_time = current_progress * new_duration
