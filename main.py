import tkinter as tk
from PIL import Image, ImageTk


def main():
    root = tk.Tk()
    root.title("Chess")
    root.geometry("300x300")

    bg_img = Image.open("img/chess-board.png")
    pawn_img = Image.open("img/black_pawn.png")
    pawn_img = pawn_img.resize((20, 20))
    bg_img.paste(pawn_img, (0, 0), pawn_img)

    img = ImageTk.PhotoImage(bg_img)
    label = tk.Label(root, image=img)
    label.pack()
    # pawn_img = tk.PhotoImage(file="img/black_pawn.gif")
    # pawn_label = tk.Label(root, image=pawn_img)
    # pawn_label.place(x=0, y=0)

    root.mainloop()

if __name__ == '__main__':
    main()
