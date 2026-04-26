from typing import Dict

from errors import CharacterError


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
