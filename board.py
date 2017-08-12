from error import InvalidFEN, InvalidNotation


class Board(object):
    """ Board class for a chess board position """

    rows = 8
    columns = 8
    players = ["w", "b"]
    files = ["a", "b", "c", "d", "e", "f", "g", "h"]
    ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]
    pieces = ["k", "q", "r", "b", "n", "p", "K", "Q", "R", "B", "N", "P"]

    def __init__(self, fen):
        self.fen = fen

    def __repr__(self):
        return self.fen

    def __getitem__(self, notation):
        self.isvalid_notation(notation)
        return self._position[notation]

    def __setitem__(self, notation, piece):
        self.isvalid_notation(notation)
        self._position[notation] = piece

    @property
    def fen(self):
        return self._fen

    @fen.setter
    def fen(self, fen):
        self._fen = fen
        fen_blocks = fen.split(sep=" ")

        if len(fen_blocks) != 6:
            raise InvalidFEN("FEN must consist of 6 blocks")

        self._position = self.encode_position(fen_blocks[0])
        if fen_blocks[1] not in self.players:
            raise InvalidFEN("Unknown player in FEN")
        if fen_blocks[2] != "-":
            if any(char not in ["K", "Q", "k", "q"] for char in fen_blocks[2]):
                raise InvalidFEN("Unrecognizable castling avalability")
        if fen_blocks[3] != "-":
            if not self.isvalid_notation(fen_blocks[3]):
                raise InvalidFEN("Unrecognizable en passant target square")
        if not fen_blocks[4].isdigit():
            raise InvalidFEN("Unknown halfmove clock")
        if not fen_blocks[5].isdigit():
            raise InvalidFEN("Unknown fullmove number")
        self.playing = fen_blocks[1]
        self.castling_availability = fen_blocks[2]
        self.enpassant_target = fen_blocks[3]
        self.halfmove_clock = int(fen_blocks[4])
        self.fullmove_number = int(fen_blocks[5])

    def encode_position(self, fen_placement):
        position = {}
        for i in range(1, 9):
            fen_placement = fen_placement.replace(str(i), "-" * i)

        fen_placement_row = fen_placement.split(sep="/")
        if len(fen_placement_row) != 8:
            raise InvalidFEN("There must be eight ranks")

        for rank, pieces_row in zip(self.ranks, fen_placement_row):
            if len(pieces_row) != 8:
                raise InvalidFEN("Rank must have eight locations")
            for file, piece in zip(self.files, pieces_row):
                if piece == "-":
                    piece = None
                position[file + rank] = piece

        return position

    def update_fen(self):
        fen = ""
        for rank in self.ranks:
            vacant = 0
            for file in self.files:
                piece = self[file + rank]
                if piece is None:
                    vacant += 1
                else:
                    if vacant != 0:
                        fen += str(vacant)
                        vacant = 0
                    fen += piece
            fen += "/"

        fen = fen[:-1] # remove trailing /
        fen += " " + self.playing
        fen += " " + self.castling_availability
        fen += " " + self.enpassant_target
        fen += " " + str(self.halfmove_clock)
        fen += " " + str(self.fullmove_number)
        self._fen = fen

    def isvalid_notation(self, notation):
        if not isinstance(notation, str):
            raise InvalidNotation(f"Notation must be in str: {notation}")
        if len(notation) != 2:
            raise InvalidNotation(f"Length of notation must be 2: {notation}")
        if notation[0] not in self.files:
            raise InvalidNotation(f"Unknown file: {notation}")
        if notation[1] not in self.ranks:
            raise InvalidNotation(f"Unknown rank: {notation}")

    def destination(self, origin, direction):
        index = self.files.index(origin[0]) + direction[1]
        if not -1 < index < 8:
            return None
        dest_file = self.files[index]

        index = self.ranks.index(origin[1]) + direction[0]
        if not -1 < index < 8:
            return None
        dest_rank = self.ranks[index]

        dest = dest_file + dest_rank
        if self.issamecolor(origin, dest):
            return None
        else:
            return dest

    def issamecolor(self, origin, destination):
        if self[origin] is None or self[destination] is None:
            return False
        elif self[origin].isupper() == self[destination].isupper():
            return True
        else:
            return False

    def isdifferentcolor(self, origin, destination):
        if self[origin] is None or self[destination] is None:
            return False
        elif self[origin].isupper() == self[destination].isupper():
            return False
        else:
            return True
