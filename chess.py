import itertools


class Chess(object):
    """
    chess match class containing currenty player,
    board state, past history of moves, etc
    """

    def __init__(self, fen):
        self.player = fen.split(sep=" ")[1]
        self._fen = fen
        self._position = self.fen2position(fen)
        self._history = [self._position]

    def fen2position(self, fen):
        position = []
        position_string = fen.split(sep=" ")[0]
        position_string = position_string.split(sep="/")
        for pos_str in position_string:
            pos = list(pos_str)
            for i, char in enumerate(pos):
                if char.isdigit():
                    pos[i] = [None for _ in range(int(char))]
            pos = list(itertools.chain.from_iterable(pos))
            position.append(pos)
        return position


def main():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    Chess(fen)

if __name__ == '__main__':
    main()