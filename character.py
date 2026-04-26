from typing import Dict

from ability_scores import AbilityScores
from character_classes import CharacterClass
from errors import CharacterError
from factory import CharacterClassFactory
from inventory import Inventory


class Character:
    """Represents a complete D&D character."""

    def __init__(
        self,
        name: str,
        race: str,
        level: int,
        character_class: CharacterClass,
        ability_scores: AbilityScores,
        inventory: Inventory | None = None,
    ) -> None:
        self.name = name
        self.race = race
        self.level = self._validate_level(level)
        self.character_class = character_class
        self.ability_scores = ability_scores
        self.inventory = inventory if inventory is not None else Inventory()

    def _validate_level(self, level: int) -> int:
        if not isinstance(level, int):
            raise CharacterError("Level must be an integer.")

        if level < 1 or level > 20:
            raise CharacterError("Level must be between 1 and 20.")

        return level

    def get_hit_points(self) -> int:
        constitution_modifier = self.ability_scores.get_modifier("CON")
        return self.character_class.calculate_starting_hp(constitution_modifier)

    def get_armor_class(self) -> int:
        return 10 + self.ability_scores.get_modifier("DEX")

    def level_up(self) -> None:
        if self.level >= 20:
            raise CharacterError("Character is already at maximum level.")

        self.level += 1

    def display_sheet(self) -> str:
        lines = [
            "=" * 40,
            f"Name: {self.name}",
            f"Race: {self.race}",
            f"Class: {self.character_class.class_name}",
            f"Level: {self.level}",
            f"HP: {self.get_hit_points()}",
            f"AC: {self.get_armor_class()}",
            "-" * 40,
            "Ability Scores:",
        ]

        for ability, score in self.ability_scores.to_dict().items():
            modifier = self.ability_scores.get_modifier(ability)
            lines.append(f"{ability}: {score} ({modifier:+})")

        lines.append("-" * 40)
        lines.append("Inventory:")

        items = self.inventory.get_items()

        if items:
            for item in items:
                lines.append(f"- {item}")
        else:
            lines.append("- Empty")

        lines.append("=" * 40)
        return "\n".join(lines)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "race": self.race,
            "level": self.level,
            "class_name": self.character_class.class_name,
            "ability_scores": self.ability_scores.to_dict(),
            "inventory": self.inventory.to_list(),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Character":
        character_class = CharacterClassFactory.create_class(data["class_name"])
        ability_scores = AbilityScores.from_dict(data["ability_scores"])
        inventory = Inventory.from_list(data["inventory"])

        return cls(
            name=data["name"],
            race=data["race"],
            level=data["level"],
            character_class=character_class,
            ability_scores=ability_scores,
            inventory=inventory,
        )
