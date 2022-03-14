from abc import ABC, abstractmethod
from exceptions import InvalidMove


class ChessPiece(ABC):
    # recalibrate for starting with 0 instead of 1
    _reverse_lookup = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
        "1": 0,
        "2": 1,
        "3": 2,
        "4": 3,
        "5": 4,
        "6": 5,
        "7": 6,
        "8": 7,
        "#": "#",
    }
    _lookup = {
        1: "a",
        2: "b",
        3: "c",
        4: "d",
        5: "e",
        6: "f",
        7: "g",
        8: "h",
        "#": "#",
    }

    def __init__(self, pos: str = None, score: int = None, white: bool = True) -> None:
        super().__init__()
        self._moved = False
        self._color = "W"
        self._team = "WHITE" if white else "BLACK"
        self._white = white
        if not white:
            self._color = "B"
        self._image = None
        self._pos = list("##")
        if pos:
            self._pos = [self._reverse_lookup[x] for x in pos]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} ({self._pos[0]}, {self._pos[1]})>"

    def __getitem__(self, val):
        return self._pos[val]

    @abstractmethod
    def _validate(self) -> bool:
        pass

    def move(self, board, pos) -> bool:
        pos = [self._reverse_lookup.get(x) for x in pos]
        return self._validate(board, pos)

    pass


class Blank(ChessPiece):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _validate(self) -> bool:
        raise InvalidMove

    def move(self) -> bool:
        raise InvalidMove

    pass


class Pawn(ChessPiece):
    def __init__(self, *args, **kwargs) -> None:
        if not kwargs.get("score"):
            kwargs["score"] = 1
        super().__init__(*args, **kwargs)
        self._name = ""
        self._image = f"{self._color}P.png"

    def _validate(self, diff_x, diff_y, attack=False, *args, **kwargs) -> bool:
        """
        Pawn moves in straight line and attacks sideways
        """
        print(f"DIFFX: {diff_x}")
        if diff_x != 0:
            print("THIS SHOULD ENGAGE")
            if not attack:
                return False
        _move_direction = 1 if self._white else -1
        if not self._moved:
            if diff_y == 1 * _move_direction or diff_y == 2 * _move_direction:
                return True
        if diff_y != 1 * _move_direction:
            return False
        return True


class Knight(ChessPiece):
    def __init__(self, *args, **kwargs) -> None:
        if not kwargs.get("score"):
            kwargs["score"] = 3
        super().__init__(*args, **kwargs)
        self._name = "N"
        self._image = f"{self._color}N.png"

    def _validate(self, diff_x, diff_y, *args, **kwargs) -> bool:
        """
        How does a knight move?
        Knight moves in a L shape line and is tricky to grasp quickly!
        """
        if (abs(diff_x) + abs(diff_y)) != 3:
            return False
        return True


class Bishop(ChessPiece):
    def __init__(self, *args, **kwargs) -> None:
        if not kwargs.get("score"):
            kwargs["score"] = 3
        super().__init__(*args, **kwargs)
        self._name = "B"
        self._image = f"{self._color}B.png"

    def _validate(self, diff_x, diff_y, *args, **kwargs) -> bool:
        """
        Bishop moves diagonally
        """
        if abs(diff_x) != abs(diff_y):
            return False
        return True


class Rook(ChessPiece):
    def __init__(self, *args, **kwargs) -> None:
        if not kwargs.get("score"):
            kwargs["score"] = 5
        super().__init__(*args, **kwargs)
        self._name = "R"
        self._image = f"{self._color}R.png"

    def _validate(self, diff_x, diff_y, *args, **kwargs) -> bool:
        """
        Rook moves staight unlimited squares within board limits
        """
        if diff_x != 0 and diff_y != 0:
            return False
        return True


class King(ChessPiece):
    def __init__(self, *args, **kwargs) -> None:
        if not kwargs.get("score"):
            kwargs["score"] = 100
        super().__init__(*args, **kwargs)
        self._name = "K"
        self._image = f"{self._color}K.png"

    def _validate(self, diff_x, diff_y, *args, **kwargs) -> bool:
        if abs(diff_x) + abs(diff_y) != 1:
            return False
        return True

    pass


class Queen(ChessPiece):
    def __init__(self, *args, **kwargs) -> None:
        if not kwargs.get("score"):
            kwargs["score"] = 9
        super().__init__(*args, **kwargs)
        self._name = "Q"
        self._image = f"{self._color}Q.png"

    def _validate(self, diff_x, diff_y, *args, **kwargs) -> bool:
        """
        Queen moves straight and diagonally
        """
        if abs(diff_x) == abs(diff_y):
            pass
        elif diff_x == 0 or diff_y == 0:
            pass
        else:
            return False
        return True
