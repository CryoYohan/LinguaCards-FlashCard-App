from tkinter import *
from random import randint
import pandas as pd
import os
import sys
#---------- Helper Function for .exe --#
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#--------------Algorithm --------------#
words_to_learn = []
current_index = -999
def generate_random_index():
    global current_index
    current_index = randint(0, len(words_to_learn) - 1)
    print(f"New Random Pair: {words_to_learn[current_index]["German"], words_to_learn[current_index]["English"]}")

def right():
    global words_to_learn, current_index
    print(f"Removed Words: {(words_to_learn[current_index]["German"], words_to_learn[current_index]["English"])}")
    del words_to_learn[current_index]

    updated_data = pd.DataFrame(words_to_learn)
    updated_data.to_csv(resource_path("data/words_to_learn.csv"), index=False)

    flip_front_card()

def wrong():
    print(f"Preserved Words: {(words_to_learn[current_index]["German"], words_to_learn[current_index]["English"])}")
    flip_front_card()

def flip_back_card():
    global current_index
    print("Flip Back Card")
    canvas.itemconfig(card, image=card_back_img)
    canvas.itemconfig(title_text, text="English", fill="WHITE")
    canvas.itemconfig(word_text, text=f"{words_to_learn[current_index]["English"]}", fill="WHITE")

def flip_front_card():
    global current_index
    countdown()
    print("Flip Front Card")
    canvas.itemconfig(card, image=card_front_img)
    canvas.itemconfig(title_text, text="German", fill="BLACK")
    canvas.itemconfig(word_text, text=f"{words_to_learn[current_index]["German"]}", fill="BLACK")

def countdown():
    generate_random_index()
    canvas.itemconfig(word_text, text=f"{words_to_learn[current_index]["German"]}", fill="BLACK")
    window.after(3000, flip_back_card)


def start():
    global words_to_learn
    try:
        print("Reading words_to_learn.csv...")
        df = pd.read_csv(resource_path("data/words_to_learn.csv"))
    except FileNotFoundError:
        print("File does not exist! Creating file now...")
        # FIX: Use resource_path for reading german_words.csv
        df = pd.read_csv(resource_path("data/german_words.csv"))
        # FIX: Use resource_path for saving words_to_learn.csv initially
        df.to_csv(resource_path("data/words_to_learn.csv"), index=False)
        print("File created!")
        words_to_learn = df.to_dict(orient="records")
    else:
        print("File exists!")
        words_to_learn = df.to_dict(orient="records")
    finally:
        countdown()
        window.mainloop()

# ---------------------- UI SETUP ------------------------#
BACKGROUND_COLOR = "#B1DDC6"
window = Tk()
window.title("Lingua - Flash Card App")
window.resizable(False, False)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Images
card_front_img = PhotoImage(file=resource_path("images/card_front.png"))
card_back_img = PhotoImage(file=resource_path("images/card_back.png"))
right_img = PhotoImage(file=resource_path("images/right.png"))
wrong_img = PhotoImage(file=resource_path("images/wrong.png"))
lingua_icon = PhotoImage(file=resource_path("images/lingua_icon.png"))

# Canvas
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400,150, font=("Arial", 40, "italic"), text="German")
word_text = canvas.create_text(400,263, font=("Arial", 60, "bold"), text="Word")


# Widgets
wrong_btn = Button(window,image=wrong_img, padx=50, highlightthickness=0, relief="flat", cursor="hand2", bd=0, command=wrong)
right_btn = Button(window, image=right_img, padx=50, highlightthickness=0, relief="flat", cursor="hand2", bd=0, command=right)

# Grid Layout
canvas.grid(row=0, column=0, columnspan=2, sticky=N)
wrong_btn.grid(row=1, column=0, stick=N)
right_btn.grid(row=1, column=1, sticky=N)

window.wm_iconphoto(True, PhotoImage(file=resource_path("images/lingua_icon.png")))


if __name__ == "__main__":
    start()