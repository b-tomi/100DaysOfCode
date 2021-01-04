# Flash Card App

import tkinter as tk
import card_engine

BG_COLOR = "#B1DDC6"
CARD_FRONT_IMAGE = "./images/card_front.png"
CARD_BACK_IMAGE = "./images/card_back.png"
WRONG_IMAGE = "./images/wrong.png"
RIGHT_IMAGE = "./images/right.png"
FONT1 = ("Arial", 40, "italic")
FONT2 = ("Arial", 60, "bold")
FROM_LANG = "French"
TO_LANG = "English"


def next_word():
    # cancel any existing timer
    if params["timer"] is not None:
        root.after_cancel(params["timer"])
    deck.next_card()
    canvas.itemconfig(bg_image, image=bg_front)
    canvas.itemconfig(lang_text, fill="black", text=FROM_LANG)
    canvas.itemconfig(word_text, fill="black", text=deck.current_card[FROM_LANG])
    # flip the card after 3 seconds, unless a button was pressed
    params["timer"] = root.after(3000, reverse_card)


def reverse_card():
    canvas.itemconfig(bg_image, image=bg_back)
    canvas.itemconfig(lang_text, fill="white", text=TO_LANG)
    canvas.itemconfig(word_text, fill="white", text=deck.current_card[TO_LANG])


def wrong():
    # just go to the next word
    next_word()


def correct():
    # remove the card from the "to learn" queue
    deck.remove_card()
    next_word()


# main window setup
root = tk.Tk()
root.title("Flash Card App")
root.iconbitmap("icon.ico")
root.geometry("900x800")
root.resizable(False, False)
root.configure(bg=BG_COLOR)

# canvas
canvas = tk.Canvas(root, width=800, height=526, bg=BG_COLOR, highlightthickness=0)
bg_front = tk.PhotoImage(file=CARD_FRONT_IMAGE)
bg_back = tk.PhotoImage(file=CARD_BACK_IMAGE)
bg_image = canvas.create_image(400, 264, image=bg_front)
lang_text = canvas.create_text(400, 150, text="", font=FONT1)
word_text = canvas.create_text(400, 283, text="", font=FONT2)
canvas.grid(row=0, column=0, columnspan=2, padx=50, pady=50)

# buttons
wrong_img = tk.PhotoImage(file=WRONG_IMAGE)
wrong_btn = tk.Button(root, image=wrong_img, highlightthickness=0, bg=BG_COLOR, relief="flat", command=wrong)
wrong_btn.grid(row=1, column=0)

right_img = tk.PhotoImage(file=RIGHT_IMAGE)
right_btn = tk.Button(root, image=right_img, highlightthickness=0, bg=BG_COLOR, relief="flat", command=correct)
right_btn.grid(row=1, column=1)

# initialize the deck of flashcards
deck = card_engine.Deck(FROM_LANG, TO_LANG)
# to avoid having to use a global variable
params = {"timer": None}
# display an initial word
next_word()

# main loop
root.mainloop()
