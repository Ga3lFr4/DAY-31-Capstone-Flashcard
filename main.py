from tkinter import *
from tkinter import messagebox
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

# WORD DATA
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
words_list = data.to_dict(orient='records')
choice = {}


# GENERATE NEW CARD

def new_card():
    global choice, flip_timer
    window.after_cancel(flip_timer)
    choice = random.choice(words_list)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=choice['French'], fill="black")
    canvas.itemconfig(displayed_image, image=flash_card_image_front)
    flip_timer = window.after(3000, flip_card)


# FLIP CARD

def flip_card():
    canvas.itemconfig(displayed_image, image=flash_card_image_back)
    canvas.itemconfig(title, fill="white", text="English")
    canvas.itemconfig(word, fill="white", text=choice['English'])

# MARK CARD AS KNOWN


def known_card():
    try:
        words_list.remove(choice)
    except ValueError:
        messagebox.showinfo(title="No more words !", message="You have learned all the words, good job!")
    new_card()

# WINDOW
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flashy")

flip_timer = window.after(3000, flip_card)

# FLASHCARD CANVAS
canvas = Canvas(bg=BACKGROUND_COLOR, width=800, height=526, highlightthickness=0)
flash_card_image_front = PhotoImage(file="images/card_front.png")
flash_card_image_back = PhotoImage(file="images/card_back.png")
displayed_image = canvas.create_image(400, 263, image=flash_card_image_front)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# BUTTONS
yes_image = PhotoImage(file="images/right.png")
yes_button = Button(image=yes_image, highlightthickness=0, relief="flat", bd=0, command=known_card)
yes_button.grid(column=1, row=1)

no_img = PhotoImage(file="images/wrong.png")
no_button = Button(image=no_img, highlightthickness=0, relief="flat", bd=0, command=new_card)
no_button.grid(column=0, row=1)

new_card()

window.mainloop()

words_to_learn = [word for word in words_list]
df = pandas.DataFrame(words_to_learn)
df.to_csv("data/words_to_learn.csv", index=False)
