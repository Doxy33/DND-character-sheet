from typing import List

from errors import CharacterError


class Inventory:
    """Represents a character inventory."""

    def __init__(self) -> None:
        self._items: List[str] = []

    def add_item(self, item: str) -> None:
        item = item.strip()

        if item:
            self._items.append(item)

    def remove_item(self, item: str) -> None:
        if item not in self._items:
            raise CharacterError(f"Item '{item}' not found in inventory.")

        self._items.remove(item)

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
