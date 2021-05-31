from tkinter import *
from pandas import read_csv, DataFrame
from random import choice
BACKGROUND_COLOR = "#B1DDC6"

# Check if we are running program for first time and there is no progress file(words_to_learn.csv)
try:
    df = read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    df = read_csv("data/french_words.csv")
# dic = df.set_index("French")["English"].to_dict() # Makes Key, Value of Column 1 and 2.
list_of_dic = df.to_dict("records")


# Generate Word
def generate_word():
    # french, english = choice(list(dic.items())) # Used to select random key, value from dic
    # return french, english
    word = choice(list_of_dic)
    print(word)
    return word


# Swap French with English after delay
def swap(english):
    canvas.itemconfigure(lang_text, text="English", fill="white")
    canvas.itemconfigure(word_text, text=english, fill="white")
    canvas.itemconfigure(canvas_image, image=back_img)
    correct_button.config(command=clicked_correct)
    wrong_button.config(command=clicked_wrong)


# On Clicking Correct
def next_card():
    correct_button.config(command="")
    wrong_button.config(command="")
    word = generate_word()
    canvas.itemconfigure(lang_text, text="French", fill="black")
    canvas.itemconfigure(word_text, text=word["French"], fill="black")
    window.after(3000, func=lambda: swap(word["English"]))
    return word


def clicked_correct():
    word = next_card()
    list_of_dic.remove(word)
    df_new = DataFrame(list_of_dic)
    df_new.to_csv("data/words_to_learn.csv", index=False)


# On Clicking Wrong
def clicked_wrong():
    next_card()


window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flash Card App")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_img)
lang_text = canvas.create_text(400, 150, text="Click any Button to", fill="black", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Play", fill="black", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

correct_img = PhotoImage(file="images/right.png")
correct_button = Button(image=correct_img, highlightthickness=0,
                        command=clicked_correct)
correct_button.grid(row=1, column=0)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=clicked_wrong)
wrong_button.grid(row=1, column=1)

window.mainloop()
