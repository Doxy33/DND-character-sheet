import os
import unittest

from ability_scores import AbilityScores
from character import Character
from factory import CharacterClassFactory
from errors import CharacterError
from storage import CharacterFileManager
from inventory import Inventory



class TestAbilityScores(unittest.TestCase):
    def setUp(self):
        self.scores = AbilityScores(15, 14, 13, 12, 10, 8)

    def test_get_score(self):
        self.assertEqual(self.scores.get_score("STR"), 15)

    def test_get_modifier(self):
        self.assertEqual(self.scores.get_modifier("STR"), 2)
        self.assertEqual(self.scores.get_modifier("CHA"), -1)

    def test_invalid_score_raises_error(self):
        with self.assertRaises(CharacterError):
            AbilityScores(40, 10, 10, 10, 10, 10)


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()

    def test_add_item(self):
        self.inventory.add_item("Sword")
        self.assertIn("Sword", self.inventory.get_items())

    def test_remove_item(self):
        self.inventory.add_item("Shield")
        self.inventory.remove_item("Shield")
        self.assertNotIn("Shield", self.inventory.get_items())


class TestCharacter(unittest.TestCase):
    def setUp(self):
        scores = AbilityScores(15, 14, 13, 12, 10, 8)
        char_class = CharacterClassFactory.create_class("fighter")
        self.character = Character("Arthas", "Human", 1, char_class, scores)

    def test_character_name(self):
        self.assertEqual(self.character.name, "Arthas")

    def test_hit_points(self):
        self.assertEqual(self.character.get_hit_points(), 11)

    def test_armor_class(self):
        self.assertEqual(self.character.get_armor_class(), 12)

    def test_level_up(self):
        self.character.level_up()
        self.assertEqual(self.character.level, 2)


class TestFileManager(unittest.TestCase):
    TEST_FILE = "test_character.json"

    def setUp(self):
        scores = AbilityScores(16, 12, 14, 10, 11, 9)
        char_class = CharacterClassFactory.create_class("wizard")
        self.character = Character("Merla", "Elf", 1, char_class, scores)
        self.character.inventory.add_item("Spellbook")

    def tearDown(self):
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_save_and_load_character(self):
        CharacterFileManager.save_to_file(self.character, self.TEST_FILE)
        loaded_character = CharacterFileManager.load_from_file(self.TEST_FILE)

        self.assertEqual(loaded_character.name, "Merla")
        self.assertEqual(loaded_character.race, "Elf")
        self.assertEqual(loaded_character.character_class.class_name, "Wizard")
        self.assertIn("Spellbook", loaded_character.inventory.get_items())


if __name__ == "__main__":
    unittest.main()
