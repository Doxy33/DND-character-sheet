import json

from ability_scores import AbilityScores
from character import Character
from errors import CharacterError
from factory import CharacterClassFactory
from storage import CharacterFileManager


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

    character = Character(
        name=name,
        race=race,
        level=level,
        character_class=character_class,
        ability_scores=ability_scores,
    )

    while True:
        item = input("Add inventory item, or press Enter to finish: ").strip()

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
                print("\nCharacter created successfully.")

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
                    filename = input("Enter filename, e.g. hero.json: ").strip()
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

        except (
            CharacterError,
            ValueError,
            FileNotFoundError,
            json.JSONDecodeError,
        ) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
