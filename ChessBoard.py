from rich.console import Console
from itertools import cycle
from Chess_Pieces.pieces import Bishop, King, Knight, Pawn, Queen, Rook
import pathlib
import pygame

BEFORECLICK_COLOR_1 = (144, 238, 144)
BEFORECLICK_COLOR_2 = (50, 205, 50)
AFTERCLICK_COLOR = (77, 219, 115)
CHECKED_COLOR = (200, 50, 50)

console = Console()


class Turn:
    def __init__(self, teams=["WHITE", "BLACK"]) -> None:
        self._iter = cycle(teams)
        self._move_no = 0
        self._turn = self._iter.__next__()

    def __repr__(self):
        return f"TURN: {self._turn} MOVE #: {self._move_no}"

    def __eq__(self, val):
        if self._turn == val.upper():
            return True
        return False

    def __next__(self):
        self._turn = self._iter.__next__()
        self._move_no += 0.5
        return self._turn

    pass


class Board:
    def __init__(self) -> None:
        self._king = [King()]


class ChessBoard:
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

    def __init__(self, display) -> None:
        self._display = display
        self._board_lookup = [
            ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"],
            ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
            ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"],
            ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"],
            ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"],
            ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"],
            ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
            ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"],
        ]
        self._board = [
            [Rook("a1"), Pawn("a2"), None, None, None, None, Pawn("a7", white=False), Rook("a8", white=False)],
            [Knight("b1"), Pawn("b2"), None, None, None, None, Pawn("b7", white=False), Knight("b8", white=False)],
            [Bishop("c1"), Pawn("c2"), None, None, None, None, Pawn("c7", white=False), Bishop("c8", white=False)],
            [King("d1"), Pawn("d2"), None, None, None, None, Pawn("d7", white=False), King("d8", white=False)],
            [Queen("e1"), Pawn("e2"), None, None, None, None, Pawn("e7", white=False), Queen("e8", white=False)],
            [Bishop("f1"), Pawn("f2"), None, None, None, None, Pawn("f7", white=False), Bishop("f8", white=False)],
            [Knight("g1"), Pawn("g2"), None, None, None, None, Pawn("g7", white=False), Knight("g8", white=False)],
            [Rook("h1"), Pawn("h2"), None, None, None, None, Pawn("h7", white=False), Rook("h8", white=False)],
        ]
        self._kings_pos = [self["d1"], self["d8"]]
        self._turn = Turn()
        self._checked = False
        self._check_attacker = []

    def __repr__(self):
        _repr = ""
        for x in self._board:
            _repr += str(x)
            _repr += "\n"
        return _repr

    def __getitem__(self, pos):
        if type(pos) is str:
            pos = [self._reverse_lookup.get(x) for x in pos]
        return self._board[pos[0]][pos[1]]

    def _parse_pos(self, pos):
        return [self._reverse_lookup.get(x) for x in pos]

    def _get(self, pos):
        x, y = pos
        return self._board[x][y]

    def _is_check(self, pos=None):
        if pos:
            piece = self._board[pos[0]][pos[1]]
        if self._checked:
            piece = self._check_attacker[0]
        for king in self._kings_pos:
            if self._validate_attack(piece, king._pos):
                self._checked = True
                self._check_attacker.append(piece)
                self._display._checked(king)
                return True, king
        return False, None

    def _compute_pos(self, piece, to_pos):
        _diff_norm_x = 0
        _diff_norm_y = 0

        _diff_x = to_pos[0] - piece._pos[0]
        _diff_y = to_pos[1] - piece._pos[1]

        if _diff_x != 0:
            _diff_norm_x = int(_diff_x / abs(_diff_x))
        if _diff_y != 0:
            _diff_norm_y = int(_diff_y / abs(_diff_y))
        _vector_length = abs(_diff_x) or abs(_diff_y)
        _pos_to_check = [
            (piece._pos[0] + _diff_norm_x * x, piece._pos[1] + _diff_norm_y * x) for x in range(1, _vector_length)
        ]
        return _diff_x, _diff_y, _pos_to_check

    def _validate_attack(self, attacking_piece, to_pos):
        defending_piece = self._board[to_pos[0]][to_pos[1]]
        if not attacking_piece:
            return False
        if not defending_piece:
            return False
        if attacking_piece._team == defending_piece._team:
            console.log("ATTACK FAILED")
            return False
        return self._validate(attacking_piece, to_pos, attack=True)

    def _attack(self, piece, from_pos, to_pos):
        """
        Method for attack vectors
        """
        console.log(f"ATTACK: {from_pos} x {to_pos}")
        self._perform_move(piece, from_pos, to_pos)
        # increment score
        return True

    def _validate(self, piece, to_pos, attack=False):
        """
        Validates if the route is clear
        """
        diff_x, diff_y, pos_to_check = self._compute_pos(piece, to_pos)
        if isinstance(piece, Knight):
            pos_to_check = []
        console.print(pos_to_check)
        for x, y in pos_to_check:
            if self._board[x][y]:
                console.log(f"FOUND: {self._board[x][y]}")
                return False
        return piece._validate(diff_x, diff_y, attack=attack)

    def _perform_move(self, piece, from_pos, to_pos):
        piece._pos = to_pos
        _temp = self._board[from_pos[0]][from_pos[1]]
        self._board[from_pos[0]][from_pos[1]] = None
        self._board[to_pos[0]][to_pos[1]] = _temp
        piece._moved = True
        next(self._turn)

    def _explicit_move(self, from_pos, to_pos):
        if from_pos == to_pos:
            return False
        piece = self._board[from_pos[0]][from_pos[1]]
        to_piece = self._board[to_pos[0]][to_pos[1]]
        if not piece:
            return False
        if piece._team != self._turn:
            return False
        if to_piece:
            # attack scanerio
            if self._validate_attack(piece, to_pos):
                return self._attack(piece, from_pos, to_pos)
            return False
        if not self._validate(piece, to_pos):
            return False

        # CHECK CONDITION HERE
        if self._checked:
            if self._is_check():
                return False
        return self._perform_move(piece, from_pos, to_pos)

    def move(self, from_pos, to_pos, parse=False):
        if parse:
            from_pos = [self._reverse_lookup.get(x) for x in from_pos]
            to_pos = [self._reverse_lookup.get(x) for x in to_pos]
        return self._explicit_move(from_pos, to_pos)

    pass


class ChessDisplay:
    def __init__(self, gameDisplay) -> None:
        self.gameDisplay = gameDisplay
        self._path = pathlib.Path("Chess_Pieces")
        self.board = ChessBoard(self)
        self._highlight_lookup = []
        self._selected = None

    def _load_piece(self, pos, color):
        x, y = pos
        pygame.draw.rect(self.gameDisplay, color, pygame.Rect(100 * x, 100 * y, 100, 100))
        piece = self.board._board[x][y]
        if piece:
            image = pygame.image.load(self._path / piece._image)
            image = pygame.transform.scale(image, (100, 100))
            self.gameDisplay.blit(image, (100 * x, 100 * y))
        return True

    def draw(self):
        _board = self.board._board
        for i in range(len(_board[0])):
            for j in range(0, 8):
                self._load_piece((i, j), color=self._select_color((i, j)))

    def _select(self, pos):
        if self._highlight_lookup:
            prev_pos = self._highlight_lookup.pop(0)
            self._load_piece(prev_pos, color=self._select_color(prev_pos))
        self._highlight_lookup.append(pos)
        self._load_piece(pos, AFTERCLICK_COLOR)
        self._selected = pos
        console.log(f"SELECTED: {pos}")
        return True

    def _checked(self, king):
        self._load_piece(king._pos, CHECKED_COLOR)
        console.log(f"CHECKED: {king} ")
        return True

    def select_or_move(self, pos):
        if self._selected:
            return self._move(pos)
        if self.board[pos]:
            return self._select(pos)
        return False

    def _select_color(self, pos):
        if sum(pos) % 2 == 0:
            return BEFORECLICK_COLOR_1
        return BEFORECLICK_COLOR_2

    def _move(self, to_pos):
        if not self._selected:
            return False
        move_flag = self.board.move(self._selected, to_pos)
        self._selected = None
        self.draw()
        if not move_flag:
            return False
        console.log(f"MOVE: {self._selected} -> {to_pos}")
        self.board._is_check(to_pos)
        return True

    pass
