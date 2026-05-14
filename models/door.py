import random


class Door:
    """
    Represents a single door in the Monty Hall game.
    Demonstrates: OOP, Encapsulation, Magic Methods
    """

    def __init__(self, number: int, has_prize: bool = False):
        self.__number = number        # Encapsulation: private attributes
        self.__has_prize = has_prize
        self.__is_open = False
        self.__is_selected = False
        self.__was_original_pick = False

    # Magic Methods
    def __str__(self):
        status = "PRIZE" if self.__has_prize else "GOAT"
        state = "open" if self.__is_open else "closed"
        return f"Door {self.__number} [{status}] ({state})"

    def __repr__(self):
        return f"Door(number={self.__number}, has_prize={self.__has_prize}, is_open={self.__is_open})"

    def __eq__(self, other):
        if isinstance(other, Door):
            return self.__number == other.__number
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Door):
            return self.__number < other.__number
        return NotImplemented

    def __hash__(self):
        return hash(self.__number)

    # Properties (Encapsulation: controlled access)
    @property
    def number(self) -> int:
        return self.__number

    @property
    def has_prize(self) -> bool:
        return self.__has_prize

    @property
    def is_open(self) -> bool:
        return self.__is_open

    @property
    def is_selected(self) -> bool:
        return self.__is_selected

    @property
    def was_original_pick(self) -> bool:
        return self.__was_original_pick

    # State management methods
    def open(self):
        self.__is_open = True

    def select(self):
        self.__is_selected = True

    def deselect(self):
        self.__is_selected = False

    def mark_as_original_pick(self):
        self.__was_original_pick = True

    def reset(self):
        self.__is_open = False
        self.__is_selected = False
        self.__was_original_pick = False
