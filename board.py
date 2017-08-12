class Board(object):
    """ Board class for a chess board position """

    rows = 8
    columns = 8
    files = ["a", "b", "c", "d", "e", "f", "g", "h"]
    ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]

    def __init__(self, fen):
        self.fen = fen

    def __repr__(self):
        return self.fen

    def __getitem__(self, notation):
        pass

    def __setitem__(self, notation, piece):
        pass

    @property
    def fen(self):
        return self._fen

    @fen.setter
    def fen(self, fen):
        pass
