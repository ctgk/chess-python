import tkinter as tk
from gui import GUI
from chess import Chess


def main():
    chess = Chess()
    print(chess.board)

    root = tk.Tk()
    root.title("Chess")
    gui = GUI(root, chess)
    gui.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
