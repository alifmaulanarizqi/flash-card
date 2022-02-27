import os
from tkinter import *
from tkinter import messagebox
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
flip_timer = None

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/words.csv")
    to_learn = data.to_dict(orient="records")
else:
    copy = data.to_dict()
    to_learn = data.to_dict(orient="records")
    print(copy)


def next_card():
    global current_card, flip_timer

    window.after_cancel(flip_timer)

    try:
        current_card = random.choice(to_learn)
    except IndexError:
        canvas.itemconfig(background_card, image=card_front_img)
        canvas.itemconfig(card_title, text="Well Done!", fill="black")
        canvas.itemconfig(card_word, text="You've memorized every card in this set.", fill="black",
                          font=("Arial", 25))
        right_button.grid(row=1, column=0, columnspan=2, pady=10)
        right_button.configure(image="", text="Reset Progress", font=("Arial", 12), width=30, pady=8)
        wrong_button.grid_forget()
    else:
        canvas.itemconfig(background_card, image=card_front_img)
        canvas.itemconfig(card_title, text="Japanese", fill="black")
        canvas.itemconfig(card_word, text=current_card["Japan"], fill="black")
        flip_timer = window.after(3000, flip_card)


def flip_card():
    # canvas.itemconfig(timer_text, text="")
    canvas.itemconfig(background_card, image=card_back_img)
    canvas.itemconfig(card_title, fill="#FFFFFF", text="English")
    canvas.itemconfig(card_word, fill="#FFFFFF", text=current_card["English"])


def is_known():
    if len(to_learn) > 0:
        to_learn.remove(current_card)
        next_card()
    else:
        if messagebox.askyesno(title="Congratulation!",
                               message="You've review all the words!\nDo you want to reset your progress?"):
            os.remove("data/words_to_learn.csv")
            window.destroy()


def save_files():
    global to_learn
    if messagebox.askyesno("Save Progress", "Do you want to save your progress?"):
        if len(to_learn) == 0:
            to_learn = {"Japan": {}, "English": {}}

        data = pd.DataFrame(to_learn)
        data.to_csv("data/words_to_learn.csv", index=False)
        window.destroy()
    else:
        window.destroy()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("FLash Card")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
background_card = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Japanese", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 40, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

right_photo = PhotoImage(file="images/right.png")
right_button = Button(image=right_photo, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=0)

wrong_photo = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_photo, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=1)

next_card()

window.protocol("WM_DELETE_WINDOW", save_files)


window.mainloop()
