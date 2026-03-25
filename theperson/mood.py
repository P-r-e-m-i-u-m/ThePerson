"""Module containing the Mood class for tracking a person's emotional state."""

from __future__ import annotations


VALID_MOODS = {
    "neutral",
    "happy",
    "sad",
    "angry",
    "anxious",
    "excited",
    "tired",
    "surprised",
    "disgusted",
    "fearful",
    "calm",
    "confused",
}


class Mood:
    """A class to represent and manage a person's mood."""

    def __init__(self,
                 name: str = "neutral",
                 intensity: float = 0.0) -> None:
        self.name = Mood._validate_name(name)
        self.intensity = self._validate_intensity(intensity)

    @staticmethod
    def _validate_name(name: str) -> str:
        if not isinstance(name, str):
            raise TypeError(
                f"Mood name must be a string, got {type(name).__name__}."
            )
        name = name.lower().strip()
        if name not in VALID_MOODS:
            raise ValueError(
                f"'{name}' is not a recognised mood. "
                f"Valid moods are: {', '.join(sorted(VALID_MOODS))}."
            )
        return name

    def _validate_intensity(self, intensity: float) -> float:
        if not isinstance(intensity, (int, float)):
            raise TypeError(
                f"Intensity must be a number, got {type(intensity).__name__}."
            )
        intensity = float(intensity)
        if not 0.0 <= intensity <= 1.0:
            raise ValueError(
                f"Intensity must be between 0 and 1, got {intensity}."
            )
        if self.name == "neutral":
            return 0.0
        return intensity

    def set_mood(self, name: str, intensity: float = 0.5) -> None:
        self.name = Mood._validate_name(name)
        self.intensity = self._validate_intensity(intensity)

    def intensify(self, amount: float = 0.1) -> None:
        if amount < 0:
            raise ValueError(
                "Amount must be non-negative. Use calm_down() to decrease intensity."
            )
        if self.name == "neutral":
            raise ValueError(
                "Cannot intensify a neutral mood. Use set_mood() first."
            )
        self.intensity = min(1.0, self.intensity + amount)

    def calm_down(self, amount: float = 0.1) -> None:
        if amount < 0:
            raise ValueError("Amount must be non-negative.")
        self.intensity = max(0.0, self.intensity - amount)
        if self.intensity == 0.0:
            self.name = "neutral"

    def reset(self) -> None:
        """Reset the mood back to neutral with zero intensity."""
        self.name = "neutral"
        self.intensity = 0.0

    def is_neutral(self) -> bool:
        """Return True if the mood is effectively neutral."""
        return self.name == "neutral" or self.intensity == 0.0

    def is_positive(self) -> bool:
        return self.name in {"happy", "excited", "calm", "surprised"}

    def is_negative(self) -> bool:
        return self.name in {
            "sad", "angry", "anxious", "tired",
            "disgusted", "fearful", "confused"
        }

    def describe(self) -> str:
        if self.is_neutral():
            return "feeling neutral."

        intensity_label = (
            "slightly" if self.intensity < 0.4
            else "moderately" if self.intensity < 0.7
            else "very"
        )

        return (
            f"feeling {intensity_label} {self.name} "
            f"(intensity: {self.intensity:.2f})."
        )

    def __str__(self) -> str:
        return self.describe()

    def __repr__(self) -> str:
        return f"Mood(name={self.name!r}, intensity={self.intensity})"

    def express(self) -> str:
        if not isinstance(self.intensity, (int, float)) or not 0.0 <= self.intensity <= 1.0:
            raise ValueError(f"Intensity must be between 0 and 1, got {self.intensity}.")

        if self.is_neutral():
            return "😐"

        level = min(10, max(1, int(self.intensity * 10) + 1))

        emoji_map = {
            "happy": ["🙂","😊","😄","😁","😆","😃","🤩","🥳","😍","🤩"],
            "sad": ["🙁","☹️","😞","😔","😢","😭","😿","😓","😩","😭"],
        }

        return emoji_map.get(self.name, ["😐"] * 10)[level - 1]
