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


class Pawn(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.abbreviation = "p" if color == "b" else "P"


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


class Queen(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.abbreviation = "q" if color == "b" else "Q"


class King(Piece):

    def __init__(self, color):
        super().__init__(color)
        self.abbreviation = "k" if color == "b" else "K"


def main():
    p = abbr2piece("P")
    print(p == "P")


if __name__ == '__main__':
    main()