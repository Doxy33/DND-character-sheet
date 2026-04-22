from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Dict, List


class CharacterError(Exception):
    """Custom exception for character-related errors."""


class AbilityScores:
    """Encapsulates and manages ability scores."""

    MIN_SCORE = 1
    MAX_SCORE = 30

    def __init__(
        self,
        strength: int,
        dexterity: int,
        constitution: int,
        intelligence: int,
        wisdom: int,
        charisma: int,
    ) -> None:
        self.__scores = {
            "STR": self._validate_score(strength),
            "DEX": self._validate_score(dexterity),
            "CON": self._validate_score(constitution),
            "INT": self._validate_score(intelligence),
            "WIS": self._validate_score(wisdom),
            "CHA": self._validate_score(charisma),
        }

    def _validate_score(self, score: int) -> int:
        if not isinstance(score, int):
            raise CharacterError("Ability score must be an integer.")
        if not self.MIN_SCORE <= score <= self.MAX_SCORE:
            raise CharacterError(
                f"Ability score must be between {self.MIN_SCORE} and {self.MAX_SCORE}."
            )
        return score

    def get_score(self, ability: str) -> int:
        return self.__scores[ability]

    def set_score(self, ability: str, score: int) -> None:
        if ability not in self.__scores:
            raise CharacterError(f"Unknown ability: {ability}")
        self.__scores[ability] = self._validate_score(score)

    def get_modifier(self, ability: str) -> int:
        return (self.get_score(ability) - 10) // 2

    def to_dict(self) -> Dict[str, int]:
        return dict(self.__scores)

    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> "AbilityScores":
        return cls(
            strength=data["STR"],
            dexterity=data["DEX"],
            constitution=data["CON"],
            intelligence=data["INT"],
            wisdom=data["WIS"],
            charisma=data["CHA"],
        )


class Inventory:
    """Represents a character inventory using composition."""

    def __init__(self) -> None:
        self._items: List[str] = []

    def add_item(self, item: str) -> None:
        item = item.strip()
        if item:
            self._items.append(item)

    def remove_item(self, item: str) -> None:
        if item in self._items:
            self._items.remove(item)
        else:
            raise CharacterError(f"Item '{item}' not found in inventory.")

    def get_items(self) -> List[str]:
        return list(self._items)

    def to_list(self) -> List[str]:
        return list(self._items)

    @classmethod
    def from_list(cls, items: List[str]) -> "Inventory":
        inventory = cls()
        for item in items:
            inventory.add_item(item)
        return inventory


class CharacterClass(ABC):
    """Abstract base class for different D&D classes."""

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


class CharacterClassFactory:
    """Factory Method pattern for creating class objects."""

    @staticmethod
    def create_class(class_name: str) -> CharacterClass:
        normalized = class_name.strip().lower()

        if normalized == "fighter":
            return Fighter()
        if normalized == "wizard":
            return Wizard()
        if normalized == "rogue":
            return Rogue()

        raise CharacterError(f"Unsupported class: {class_name}")


class Character:
    """Represents a D&D character."""

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


class CharacterFileManager:
    """Handles reading and writing characters to JSON files."""

    @staticmethod
    def save_to_file(character: Character, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(character.to_dict(), file, indent=4)

    @staticmethod
    def load_from_file(filename: str) -> Character:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        return Character.from_dict(data)


def create_character_from_input() -> Character:
    """Create a new character from user input."""
    print("Create your D&D character")
    name = input("Enter character name: ").strip()
    race = input("Enter race: ").strip()
    class_name = input("Enter class (Fighter/Wizard/Rogue): ").strip()
    level = int(input("Enter level (1-20): ").strip())

    print("Enter ability scores:")
    strength = int(input("STR: "))
    dexterity = int(input("DEX: "))
    constitution = int(input("CON: "))
    intelligence = int(input("INT: "))
    wisdom = int(input("WIS: "))
    charisma = int(input("CHA: "))

    ability_scores = AbilityScores(
        strength=strength,
        dexterity=dexterity,
        constitution=constitution,
        intelligence=intelligence,
        wisdom=wisdom,
        charisma=charisma,
    )

    character_class = CharacterClassFactory.create_class(class_name)
    character = Character(name, race, level, character_class, ability_scores)

    while True:
        item = input("Add an inventory item (or press Enter to finish): ").strip()
        if not item:
            break
        character.inventory.add_item(item)

    return character


def main() -> None:
    """Main menu for the application."""
    current_character = None

    while True:
        print("\nD&D Character Sheet Creator")
        print("1. Create character")
        print("2. View character sheet")
        print("3. Save character")
        print("4. Load character")
        print("5. Level up character")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                current_character = create_character_from_input()
                print("\nCharacter created successfully!")

            elif choice == "2":
                if current_character is None:
                    print("No character loaded.")
                else:
                    print()
                    print(current_character.display_sheet())

            elif choice == "3":
                if current_character is None:
                    print("No character to save.")
                else:
                    filename = input("Enter filename to save (e.g. hero.json): ").strip()
                    CharacterFileManager.save_to_file(current_character, filename)
                    print("Character saved successfully.")

            elif choice == "4":
                filename = input("Enter filename to load: ").strip()
                current_character = CharacterFileManager.load_from_file(filename)
                print("Character loaded successfully.")

            elif choice == "5":
                if current_character is None:
                    print("No character loaded.")
                else:
                    current_character.level_up()
                    print(f"{current_character.name} is now level {current_character.level}.")

            elif choice == "6":
                print("Exiting program.")
                break

            else:
                print("Invalid option. Please try again.")

        except (CharacterError, ValueError, FileNotFoundError, json.JSONDecodeError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()