from abc import ABC, abstractmethod


class CharacterClass(ABC):
    """Abstract base class for D&D classes."""

    def __init__(self, class_name: str, hit_die: int) -> None:
        self.class_name = class_name
        self.hit_die = hit_die

    @abstractmethod
    def calculate_starting_hp(self, constitution_modifier: int) -> int:
        """Calculate starting hit points."""


class Fighter(CharacterClass):
    """Concrete class representing Fighter."""

    def __init__(self) -> None:
        super().__init__("Fighter", 10)

    def calculate_starting_hp(self, constitution_modifier: int) -> int:
        return self.hit_die + constitution_modifier


class Wizard(CharacterClass):
    """Concrete class representing Wizard."""

    def __init__(self) -> None:
        super().__init__("Wizard", 6)

    def calculate_starting_hp(self, constitution_modifier: int) -> int:
        return self.hit_die + constitution_modifier


class Rogue(CharacterClass):
    """Concrete class representing Rogue."""

    def __init__(self) -> None:
        super().__init__("Rogue", 8)

    def calculate_starting_hp(self, constitution_modifier: int) -> int:
        return self.hit_die + constitution_modifier
