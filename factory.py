from character_classes import CharacterClass, Fighter, Rogue, Wizard
from errors import CharacterError


class CharacterClassFactory:
    """Factory Method pattern for creating character class objects."""

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
