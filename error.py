class ChessError(Exception):
    pass


class Check(ChessError):
    pass


class ColorError(ChessError):
    pass


class InvalidFEN(ChessError):
    pass


class InvalidMove(ChessError):
    pass


class InvalidNotation(ChessError):
    pass


class InvalidPiece(ChessError):
    pass


class NotYourTurn(ChessError):
    pass
