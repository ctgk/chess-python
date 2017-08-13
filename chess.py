from copy import deepcopy
from board import Board
from error import InvalidMove, NotYourTurn


class Chess(object):
    """ class for a chess game """

    files = ["a", "b", "c", "d", "e", "f", "g", "h"]
    ranks = ["8", "7", "6", "5", "4", "3", "2", "1"]
    initial_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

    def __init__(self, fen=None):
        if fen is None:
            fen = self.initial_fen
        self.board = Board(fen)
        self.history = []

    def move(self, origin, dest):
        piece = self.board[origin]

        # if no piece at the origin, exit
        if piece is None:
            return 0

        # raise error if it's not the player's turn
        played = piece.color
        if played != self.board.playing:
            color = "white" if played == "w" else "black"
            raise NotYourTurn(f"It's not {color}'s turn")

        if dest not in piece.possible_moves():
            raise InvalidMove(f"{origin} cannot move to {dest}")

        # update board
        self.history.append(deepcopy(self.board))
        piece.move_to(dest)

        # update player turn
        self.board.playing = "w" if piece.color == "b" else "b"

        # update en passant target square
        if piece.name != "Pawn":
            self.board.enpassant_target = "-"

        # update halfmove clock
        if self.history[-1][dest] is None and piece.name != "Pawn":
            self.board.halfmove_clock += 1
        else:
            self.board.halfmove_clock = 0

        # update fullmove number
        if piece.color == "b":
            self.board.fullmove_number += 1

        self.board.update_fen()


def main():
    Chess()


if __name__ == '__main__':
    main()
