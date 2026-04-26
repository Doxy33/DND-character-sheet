import json

from character import Character


class CharacterFileManager:
    """Handles reading and writing character data."""

    @staticmethod
    def save_to_file(character: Character, filename: str) -> None:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(character.to_dict(), file, indent=4)

    @staticmethod
    def load_from_file(filename: str) -> Character:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        return Character.from_dict(data)
