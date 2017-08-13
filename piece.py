from error import ColorError, InvalidPiece


def abbr2piece(abbreviation):
    abbr = abbreviation.lower()
    color = "w" if abbreviation.isupper() else "b"
    if abbr == "-":
        return None
    elif abbr == "p":
        return Pawn(color)
    elif abbr == "n":
        return Knight(color)
    elif abbr == "b":
        return Bishop(color)
    elif abbr == "r":
        return Rook(color)
    elif abbr == "q":
        return Queen(color)
    elif abbr == "k":
        return King(color)
    else:
        raise InvalidPiece(f"Unknown piece: {abbreviation}")


class Piece(object):
    """ base class of chess pieces """

    def __init__(self, color):
        if color not in ["w", "b"]:
            raise ColorError(f"Unknown color: {color}")
        self.color = color # which color white or black

    def __repr__(self):
        return self.abbreviation

    def __eq__(self, other):
        if isinstance(other, Piece):
            return self.__dict__ == other.__dict__
        elif isinstance(other, str):
            return other == self.abbreviation
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def name(self):
        return self.__class__.__name__

    def place_at(self, position, board=None):
        if board is not None:
            self.board = board
        self.board[position] = self
        self.position = position
        self.home = position

    def move_to(self, dest):
        captured = self.board.isdifferentcolor(self.position, dest)
        self.board[dest] = self
        self.board[self.position] = None
        self.position = dest


class Pawn(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.abbreviation = "p" if color == "b" else "P"

    def possible_moves(self):
        moves = []
        file = self.position[0]
        rank = self.position[1]
        sign = -1 if self.color == "w" else 1

        # standard move
        dest = self.board.destination(self.position, (sign, 0))
        if dest is not None:
            moves.append(dest)

            # moving two squares
            if self.position == self.home:
                dest = self.board.destination(self.position, (2 * sign, 0))
                if dest is not None:
                    moves.append(dest)

        # attacking moves
        dest_candidates = [
            self.board.destination(self.position, (sign, d)) for d in [-1, 1]
        ]
        for cand in dest_candidates:
            if cand is None:
                continue
            if self.board.isdifferentcolor(self.position, cand):
                moves.append(cand)
            if self.board.enpassant_target == cand:
                moves.append(cand)

        return moves

    def move_to(self, dest):
        # next en passant target square
        if self.position == self.home and dest[1] in ["4", "5"]:
            enpassant_target = self.home[0] + ("3" if dest[1] == "4" else "6")
        else:
            enpassant_target = "-"

        # move this piece
        super().move_to(dest)

        # promotion
        if self.position[1] in ["1", "8"]:
            q = Queen(self.color)
            q.place_at(self.position, self.board)
            del self

        # en passant capturing
        if dest == self.board.enpassant_target:
            sign = -1 if self.color == "w" else 1
            enemy_position = self.board.destination(dest, (-sign, 0))
            self.board[enemy_position] = None

        # update en passant target square
        self.board.enpassant_target = enpassant_target


class Knight(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.abbreviation = "n" if color == "b" else "N"


class Bishop(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.abbreviation = "b" if color == "b" else "B"


class Rook(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.abbreviation = "r" if color == "b" else "R"

    def move_to(self, dest):
        # erase castiling availability
        if self.color == "w":
            home_rank = "1"
            letters = ["K", "Q"]
        else:
            home_rank = "8"
            letters = ["k", "q"]
        if self.position == "h" + home_rank:
            self.board.castling = self.board.castling.replace(letters[0], "")
        elif self.position == "a" + home_rank:
            self.board.castling = self.board.castling.replace(letters[1], "")

        super().move_to(dest)


class Queen(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.abbreviation = "q" if color == "b" else "Q"


class King(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.abbreviation = "k" if color == "b" else "K"

    def move_to(self, dest):
        # castling
        if self.color == "w":
            home_rank = "1"
            table = str.maketrans({"K": "", "Q": ""})
        else:
            home_rank = "8"
            table = str.maketrans({"k": "", "q": ""})

        if self.position == self.home:
            self.board.castling = self.board.castling.translate(table)

        if self.position == self.home and dest == "g" + home_rank:
            self.board["h" + home_rank].move_to("f" + home_rank)
        elif self.position == self.home and dest == "c" + home_rank:
            self.board["a" + home_rank].move_to("d" + home_rank)

        super().move_to(dest)


def main():
    p = abbr2piece("P")
    print(p == "P")


if __name__ == '__main__':
    main()