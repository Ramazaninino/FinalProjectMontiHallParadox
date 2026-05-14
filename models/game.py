import random
from abc import ABC, abstractmethod
from models.door import Door


class BaseGame(ABC):
    """
    Abstract base class for all Monty Hall game variants.
    Demonstrates: Inheritance, Polymorphism, Encapsulation, Magic Methods, OOP
    """

    def __init__(self, game_id: int, name: str, door_count: int):
        self._game_id = game_id
        self._name = name
        self._door_count = door_count
        self._doors: list[Door] = []
        self._total_rounds = 0
        self._wins = 0
        self._current_selected: Door | None = None
        self._monty_opened: list[Door] = []
        self._phase = "select"  # select -> switch_or_keep -> result
        self._last_switched = False
        self._setup_doors()

    # Magic Methods
    def __str__(self):
        return (f"{self.__class__.__name__}(id={self._game_id}, "
                f"name='{self._name}', doors={self._door_count}, "
                f"wins={self._wins}/{self._total_rounds})")

    def __repr__(self):
        return f"{self.__class__.__name__}(game_id={self._game_id}, door_count={self._door_count})"

    def __len__(self):
        return self._door_count

    def __contains__(self, door_number: int):
        return 1 <= door_number <= self._door_count

    # Properties (Encapsulation)
    @property
    def game_id(self) -> int:
        return self._game_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def door_count(self) -> int:
        return self._door_count

    @property
    def total_rounds(self) -> int:
        return self._total_rounds

    @property
    def wins(self) -> int:
        return self._wins

    @property
    def win_rate(self) -> float:
        if self._total_rounds == 0:
            return 0.0
        return round(self._wins / self._total_rounds * 100, 1)

    @property
    def doors(self) -> list[Door]:
        return self._doors

    @property
    def phase(self) -> str:
        return self._phase

    @property
    def current_selected(self) -> Door | None:
        return self._current_selected

    @property
    def monty_opened(self) -> list[Door]:
        return self._monty_opened

    @property
    def last_switched(self) -> bool:
        return self._last_switched

    # Core game logic
    def _setup_doors(self):
        """Create N doors, one randomly has a prize."""
        prize_index = random.randint(0, self._door_count - 1)
        self._doors = [
            Door(i + 1, has_prize=(i == prize_index))
            for i in range(self._door_count)
        ]
        self._monty_opened = []
        self._current_selected = None
        self._original_selected = None
        self._phase = "select"

    def _monty_opens_doors(self):
        """
        Monty opens exactly ONE losing door that:
          - is not the player's chosen door
          - does not have the prize
        This keeps all other doors closed so the player can choose
        which door to switch to (more interactive, classic UX).
        """
        losers = [
            d for d in self._doors
            if not d.has_prize and not d.is_selected
        ]
        revealed = random.choice(losers)
        revealed.open()
        self._monty_opened = [revealed]

    def select_door(self, door_number: int) -> bool:
        """Player picks a door. Returns True if selection succeeded."""
        if self._phase != "select":
            return False
        if door_number not in self:
            return False

        for door in self._doors:
            door.deselect()

        selected = self._doors[door_number - 1]
        selected.select()
        selected.mark_as_original_pick()
        self._current_selected = selected
        self._original_selected = selected   # remember first pick
        self._monty_opens_doors()
        self._phase = "switch_or_keep"
        return True

    def switch_door(self, door_number: int) -> bool:
        """
        Player switches to a specific door by number.
        The door must be closed and not currently selected.
        Returns win result.
        """
        if self._phase != "switch_or_keep":
            return False
        if door_number < 1 or door_number > self._door_count:
            return False

        target = self._doors[door_number - 1]
        if target.is_selected or target.is_open:
            return False

        self._current_selected.deselect()
        target.select()
        self._current_selected = target
        self._last_switched = True
        return self._resolve_result()

    def keep_door(self) -> bool:
        """Player keeps current door. Returns win result."""
        if self._phase != "switch_or_keep":
            return False
        self._last_switched = False
        return self._resolve_result()

    def _resolve_result(self) -> bool:
        """Open selected door, original door, and the prize door."""
        self._current_selected.open()

        # Show the original first pick (if player switched)
        if self._original_selected and not self._original_selected.is_open:
            self._original_selected.open()

        # Reveal the prize door so player sees where it was
        for door in self._doors:
            if door.has_prize and not door.is_open:
                door.open()

        won = self._current_selected.has_prize
        self._total_rounds += 1
        if won:
            self._wins += 1
        self._phase = "result"
        return won

    def new_round(self):
        """Start a new round within the same game session."""
        self._setup_doors()

    # Polymorphism: subclasses must implement this
    @abstractmethod
    def get_mode(self) -> str:
        pass

    @abstractmethod
    def get_mode_label(self) -> str:
        pass


class ManualGame(BaseGame):
    """
    Manual mode: the player manually chooses doors each round.
    Demonstrates: Inheritance, Polymorphism
    """

    def __init__(self, game_id: int, name: str, door_count: int):
        super().__init__(game_id, name, door_count)

    def get_mode(self) -> str:
        return "manual"

    def get_mode_label(self) -> str:
        return "Ручной"

    def __str__(self):
        base = super().__str__()
        return f"Manual{base}"


class AutoGame(BaseGame):
    """
    Auto mode: computer simulates N games automatically.
    Compares 'always switch' vs 'always stay' strategies.
    Demonstrates: Inheritance, Polymorphism
    """

    def __init__(self, game_id: int, name: str, door_count: int, num_games: int):
        self._num_games = num_games
        self._simulation_done = False
        super().__init__(game_id, name, door_count)

    @property
    def num_games(self) -> int:
        return self._num_games

    def simulate(self) -> dict:
        """
        Run N simulations: randomly pick a door, check if it has the prize.
        Win rate approaches 1/door_count (pure random guessing).
        """
        wins = 0

        for _ in range(self._num_games):
            prize_door = random.randint(1, self._door_count)
            player_pick = random.randint(1, self._door_count)
            if player_pick == prize_door:
                wins += 1

        self._total_rounds = self._num_games
        self._wins = wins
        self._simulation_done = True

        return {
            "total": self._num_games,
            "wins": wins,
            "win_rate": round(wins / self._num_games * 100, 1),
        }

    def get_mode(self) -> str:
        return "auto"

    def get_mode_label(self) -> str:
        return "Авто"

    def __str__(self):
        base = super().__str__()
        return f"Auto{base}[games={self._num_games}]"
