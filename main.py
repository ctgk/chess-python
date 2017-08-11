import tkinter as tk
from board import Board
from chess import Chess


def main():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    chess = Chess(fen)

    root = tk.Tk()
    root.title("Chess")
    board = Board(root, chess)
    board.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
