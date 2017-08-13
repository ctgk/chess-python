from copy import deepcopy
from board import Board
from error import NotYourTurn, InvalidMove
from piece import abbr2piece


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

        if dest not in self.available_moves(origin):
            raise InvalidMove(f"{origin} cannot move to {dest}")

        # update board
        self.history.append(deepcopy(self.board))
        self.board[origin] = None
        self.board[dest] = piece
        # castling
        if piece == "K" and origin == "e1" and dest == "g1":
            self.board["h1"] = None
            self.board["f1"] = abbr2piece("R")
        elif piece == "K" and origin == "e1" and dest == "c1":
            self.board["a1"] = None
            self.board["d1"] = abbr2piece("R")
        elif piece == "k" and origin == "e8" and dest == "g8":
            self.board["h8"] = None
            self.board["f8"] = abbr2piece("r")
        elif piece == "k" and origin == "e8" and dest == "c8":
            self.board["a8"] = None
            self.board["d8"] = abbr2piece("r")

        # player turn
        self.board.playing = "w" if played == "b" else "b"

        # castling availability
        castling = self.board.castling_availability
        if piece == "K":
            castling = castling.replace("K", "")
            castling = castling.replace("Q", "")
        elif piece == "k":
            castling = castling.replace("k", "")
            castling = castling.replace("q", "")
        elif piece == "R":
            if origin == "h1":
                castling = castling.replace("K", "")
            elif origin == "a1":
                castling = castling.replace("Q", "")
        elif piece == "r":
            if origin == "h8":
                castling = castling.replace("k", "")
            elif origin == "a8":
                castling = castling.replace("q", "")
        if castling == "":
            castling = "-"
        self.board.castling_availability = castling

        # en passant target
        if piece == "p" and origin[1] == "7" and dest[1] == "5":
            self.board.enpassant_target = origin[0] + "6"
        elif piece == "P" and origin[1] == "2" and dest[1] == "4":
            self.board.enpassant_target = origin[0] + "3"
        else:
            self.board.enpassant_target = "-"

        # halfmove clock
        if self.history[-1][dest] is None and piece.name != "Pawn":
            self.board.halfmove_clock += 1
        else:
            self.board.halfmove_clock = 0

        # fullmove number
        if played == "b":
            self.board.fullmove_number += 1

        self.board.update_fen()

    def available_moves(self, origin):
        piece = self.board[origin]

        if piece is None:
            return []
        elif piece.name == "Pawn":
            return self.pawn_moves(origin)
        elif piece.name == "Knight":
            return self.knight_moves(origin)
        elif piece.name == "Bishop":
            return self.bishop_moves(origin)
        elif piece.name == "Rook":
            return self.rook_moves(origin)
        elif piece.name == "Queen":
            return self.queen_moves(origin)
        elif piece.name == "King":
            return self.king_moves(origin)
        else:
            raise NotImplementedError

    def pawn_moves(self, origin):
        moves = []
        color = self.board[origin].color
        file = origin[0]
        rank = origin[1]
        sign = -1 if color == "w" else 1

        # standard move
        dest = self.board.destination(origin, (sign, 0))
        if dest is not None:
            moves.append(dest)

            # moving two squares
            if (color == "w" and rank == "2") or (color == "b" and rank == "7"):
                dest = self.board.destination(origin, (2 * sign, 0))
                if dest is not None:
                    moves.append(dest)

        # attacking moves
        dest_candidates = [
            self.board.destination(origin, (sign, d)) for d in [-1, 1]
        ]
        for cand in dest_candidates:
            if cand is None:
                continue
            if self.board.isdifferentcolor(origin, cand):
                moves.append(cand)

        return moves

    def knight_moves(self, origin):
        directions = [
            (-2, -1), (-2, 1), # forward (from white's perspective)
            (-1, 2), (1, 2), # right
            (2, 1), (2, -1), # backward
            (1, -2), (-1, -2) # left
        ]
        moves = [self.board.destination(origin, d) for d in directions]
        return list(filter(None, moves))

    def bishop_moves(self, origin):
        directions = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        moves = []

        for d in directions:
            current = deepcopy(d)
            while True:
                dest = self.board.destination(origin, current)
                if dest is None:
                    break
                moves.append(dest)
                if self.board.isdifferentcolor(origin, dest):
                    break
                current = [x + y for x, y in zip(d, current)]
        return moves

    def rook_moves(self, origin):
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        moves = []

        for d in directions:
            current = deepcopy(d)
            while True:
                dest = self.board.destination(origin, current)
                if dest is None:
                    break
                moves.append(dest)
                if self.board.isdifferentcolor(origin, dest):
                    break
                current = [x + y for x, y in zip(d, current)]
        return moves

    def queen_moves(self, origin):
        return self.bishop_moves(origin) + self.rook_moves(origin)

    def king_moves(self, origin):
        moves = []
        color = self.board[origin].color
        side = ("K", "Q") if color == "w" else ("k", "q")
        rank = "1" if color == "w" else "8"

        if (
            side[0] in self.board.castling_availability
            and self.board["f" + rank] is None
            and self.board["g" + rank] is None
        ):
            moves.append("g" + rank)
        if (
            side[1] in self.board.castling_availability
            and self.board["d" + rank] is None
            and self.board["c" + rank] is None
            and self.board["b" + rank] is None
        ):
            moves.append("c" + rank)

        directions = [
            [-1, -1], [-1, 0], [-1, 1],
            [0, -1], [0, 1],
            [1, -1], [1, 0], [1, 1]
        ]
        moves += [self.board.destination(origin, d) for d in directions]
        return list(filter(None, moves))


def main():
    Chess()


if __name__ == '__main__':
    main()