from rich.console import Console
from itertools import cycle
from Chess_Pieces.pieces import Bishop, King, Knight, Pawn, Queen, Rook
import pathlib
import pygame

BEFORECLICK_COLOR_1 = (144, 238, 144)
BEFORECLICK_COLOR_2 = (50, 205, 50)
AFTERCLICK_COLOR = (77, 219, 115)
CHECKED_COLOR = (200, 50, 50)
POSSIBLECOLOR = (55, 40, 250)

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
    _lookup = {
        0: "a",
        1: "b",
        2: "c",
        3: "d",
        4: "e",
        5: "f",
        6: "g",
        7: "h",
    }

    def __init__(self, display, turn=True) -> None:
        self._display = display
        self._board = [
            [Rook("a1"), Pawn("a2"), None, None, None, None, Pawn("a7", white=False), Rook("a8", white=False)],
            [Knight("b1"), Pawn("b2"), None, None, None, None, Pawn("b7", white=False), Knight("b8", white=False)],
            [Bishop("c1"), Pawn("c2"), None, None, None, None, Pawn("c7", white=False), Bishop("c8", white=False)],
            [Queen("d1"), Pawn("d2"), None, None, None, None, Pawn("d7", white=False), Queen("d8", white=False)],
            [King("e1"), Pawn("e2"), None, None, None, None, Pawn("e7", white=False), King("e8", white=False)],
            [Bishop("f1"), Pawn("f2"), None, None, None, None, Pawn("f7", white=False), Bishop("f8", white=False)],
            [Knight("g1"), Pawn("g2"), None, None, None, None, Pawn("g7", white=False), Knight("g8", white=False)],
            [Rook("h1"), Pawn("h2"), None, None, None, None, Pawn("h7", white=False), Rook("h8", white=False)],
        ]
        self._kings_pos = [self["d1"], self["d8"]]
        self._turn = Turn() if turn else None
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

    def _reparse_pos(self, pos):
        return f"{self._lookup.get(pos[0])}{pos[1] + 1}"

    def get(self, pos):
        x, y = pos
        return self._board[x][y]

    def _is_check(self, pos=None):
        if pos:
            piece = self._board[pos[0]][pos[1]]
        if self._checked:
            piece = self._check_attacker[0]
        # for king in self._kings_pos:
        #     if self._validate_attack(piece, king._pos):
        #         self._checked = True
        #         self._check_attacker.append(piece)
        #         self._display._checked(king)
        #         return True, king
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
            (piece._pos[0] + _diff_norm_x * (1 + x), piece._pos[1] + _diff_norm_y * (1 + x))
            for x in range(0, _vector_length)
        ]
        return _diff_x, _diff_y, _pos_to_check

    def _validate_attack(self, attacking_piece, to_pos):
        defending_piece = self._board[to_pos[0]][to_pos[1]]
        if not attacking_piece:
            return False
        if not defending_piece:
            return False
        if attacking_piece._team == defending_piece._team:
            console.log("SELF TEAM ATTACK (FAILED)")
            return False
        return self._validate(attacking_piece, to_pos, attack=True)

    def _opossible_moves(self, piece):
        diffs_x, diffs_y = piece._possibles()
        for diff_x in diffs_x:
            for diff_y in diffs_y:
                _current_pos = piece._pos
                to_pos = (diff_x + _current_pos[0], diff_y + _current_pos[1])
                console.log(f"POSSILE: {to_pos}")
                if to_pos[0] > 7 or to_pos[1] > 7:
                    continue
                if not self._validate(piece, to_pos):
                    break
                _current_pos = to_pos
                yield to_pos

    def _possible_moves(self, piece):
        for x in range(0, 8):
            for y in range(0, 8):
                to_pos = (x, y)
                if self._validate(piece, to_pos):
                    yield to_pos

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
        if piece._pos == to_pos:
            return False
        diff_x, diff_y, pos_to_check = self._compute_pos(piece, to_pos)
        if isinstance(piece, Knight):
            pos_to_check = [to_pos]

        defending_piece = self.get(to_pos)
        if defending_piece:
            if defending_piece._team != piece._team:
                console.log(pos_to_check, to_pos)
                if to_pos in pos_to_check:
                    pos_to_check.remove(to_pos)
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
        if self._turn:
            next(self._turn)
        console.log(f"PERFORMED MOVE: {self._reparse_pos(from_pos)} -> {self._reparse_pos(to_pos)}")
        return True

    def _explicit_move(self, from_pos, to_pos):
        if from_pos == to_pos:
            console.log("same pos")
            return False
        piece = self._board[from_pos[0]][from_pos[1]]
        to_piece = self._board[to_pos[0]][to_pos[1]]
        if not piece:
            console.log("piece not found")
            return False
        if self._turn:
            if piece._team != self._turn:
                console.log("not your turn")
                return False
        if to_piece:
            # attack scanerio
            if self._validate_attack(piece, to_pos):
                return self._attack(piece, from_pos, to_pos)
            console.log("attack failed")
            return False
        if not self._validate(piece, to_pos):
            console.log("piece validation failed")
            return False

        # CHECK CONDITION HERE
        if self._checked:
            if self._is_check():
                console.log("under check")
                return False
        return self._perform_move(piece, from_pos, to_pos)

    def move(self, from_pos, to_pos, parse=False):
        if parse:
            from_pos = [self._reverse_lookup.get(str(x)) for x in from_pos]
            to_pos = [self._reverse_lookup.get(str(x)) for x in to_pos]
        return self._explicit_move(from_pos, to_pos)

    pass


class ChessDisplay:
    _position_bridge = {0: 7, 1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 0}
    _position_bridge_reverse = dict({v: k for k, v in _position_bridge.items()})

    def __init__(self, gameDisplay) -> None:
        self.gameDisplay = gameDisplay
        self._path = pathlib.Path("Chess_Pieces")
        self.board = ChessBoard(self)
        self._highlight_lookup = []
        self._selected = None

    def _pos_bridge(self, pos, reverse=False):
        if reverse:
            return (pos[0], self._position_bridge_reverse[pos[1]])
        return (pos[0], self._position_bridge[pos[1]])

    def _load_piece(self, pos, color):
        x, y = pos
        pygame.draw.rect(self.gameDisplay, color, pygame.Rect(100 * x, 100 * y, 100, 100))
        _bridged_position = self._pos_bridge(pos)
        piece = self.board._board[_bridged_position[0]][_bridged_position[1]]
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
        console.log(f"SELECTED: {self._selected}")

        _possible_moves = self.board._possible_moves(self.board.get(self._pos_bridge(self._selected, reverse=True)))
        for _possible in _possible_moves:
            # POSSIBLECOLOR for possible positions // no piece
            _possible = self._pos_bridge(_possible)
            self._load_piece(_possible, POSSIBLECOLOR)
        return True

    def _checked(self, king):
        self._load_piece(king._pos, CHECKED_COLOR)
        console.log(f"CHECKED: {king} ")
        return True

    def select_or_move(self, pos):
        if self._selected:
            console.log("attempting move")
            return self._move(pos)
        if self.board[self._pos_bridge(pos, reverse=True)]:
            console.log("attempting select")
            return self._select(pos)
        return False

    def _select_color(self, pos):
        if sum(pos) % 2 == 0:
            return BEFORECLICK_COLOR_1
        return BEFORECLICK_COLOR_2

    def _move(self, to_pos):
        if not self._selected:
            return False
        from_pos = self._selected
        move_flag = self.board.move(self._pos_bridge(from_pos, reverse=True), self._pos_bridge(to_pos, reverse=True))
        self._selected = None
        self.draw()
        if not move_flag:
            return False
        console.log(f"MOVE: {from_pos} -> {to_pos}")
        self.board._is_check(to_pos)
        return True

    pass
