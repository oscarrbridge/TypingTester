"""
This is a program to help users improve their typing skills
"""
from tkinter import *
import tkinter as tk
from random import randint
window = tk.Tk()

the_words = []
game_running = False

count, full_count, fails, score = 0, 0, 0, 0


def mouse_clicked(_):
    """
    Is called when mouse is clicked,
    This function checks if the game is running,
    if not the game will restart
    :return:
    """
    global game_running

    if game_running is False:
        game_running = True
        start_test()

    if game_running is True and full_count == 0:
        restart_test()


def start_test():
    """
    Starts countdown timer, calls word list and resets all the variables
    :return:
    """
    global full_count, count, fails, score

    # Resets variables
    count = 1
    full_count = 30
    fails = 0
    score = 0

    # Deleting end screen widgets
    done_label.grid_forget()
    replay_label.grid_forget()
    results_label.grid_forget()
    wpm_label.grid_forget()
    accuracy_label.grid_forget()
    wpm_text_label.grid_forget()
    accuracy_tex_label.grid_forget()

    # Placing short countdown for user to get ready
    countdown_label.grid()
    start_timer()

    # Creating a new word list and starting the full countdown
    window.after(3000, get_word_list)
    window.after(3000, full_timer)


def start_timer():
    global count
    """
    Starts the 3 second timer for player to get ready
    :return:
    """

    countdown_label['text'] = count
    countdown_label.config(font=("Courier", 8))

    if count == 0:
        return True

    if count != 0:
        count -= 1
        window.after(1000, start_timer)


def full_timer():
    global full_count, game_running

    full_countdown_label['text'] = full_count
    full_countdown_label.grid()
    full_countdown_label.config(font=("Courier", 8))

    if full_count == 0:
        game_running = False
        restart_test()

    if full_count != 0:
        full_count -= 1
        window.after(1000, full_timer)


def restart_test():
    """
    Shows end game screen waits for user to click to restart test
    :return:
    """
    global game_running, wpm_label, accuracy_label

    # Gets wpm and accuracy to display on end screen
    calc_wpm()
    calc_acc()
    wpm_label = Label(window, text=wpm.get())
    accuracy_label = Label(window, text=accuracy.get())

    # Deletes widgets from game
    enter_box.grid_forget()
    shown_word_label.grid_forget()
    full_countdown_label.grid_forget()

    # Shows end screen widgets
    done_label.grid(row="1", column="1", columnspan="2")
    replay_label.grid(row="2", column="1", columnspan="2")
    results_label.grid(row="3", column="1", columnspan="2")
    wpm_text_label.grid(row="4", column="1")
    accuracy_tex_label.grid(row="4", column="2")
    wpm_label.grid(row="5", column="1")
    accuracy_label.grid(row="5", column="2")

    game_running = False


def get_word_list():
    """
    Gets the text file and splits words up into a list
    Display first word
    :return:
    """
    global shown_word_label

    # Delete start screen widgets for game to start
    welcome_text.grid_forget()
    countdown_label.grid_forget()

    # Change .txt file to list
    with open('words.txt', 'r') as f:
        for line in f:
            for word in line.split():
                the_words.append(word)

    # Choosing the first word to show
    shown_word.set(the_words[randint(0, len(the_words) - 1)])

    # Styling and placing needed widgets for the game
    enter_box.config(font=("Courier", 11), justify="center")
    enter_box.grid(row='2')
    shown_word_label = Label(window, text=shown_word.get())
    shown_word_label.config(font=("Courier", 11))
    shown_word_label.grid(row='1')
    display_word()


def display_word():
    """
    Shows words for user to type
    :return:
    """
    global shown_word_label

    # Changing the current word
    shown_word_label.grid_forget()
    shown_word.set(the_words[randint(0, len(the_words) - 1)])
    shown_word_label = Label(window, text=shown_word.get())
    shown_word_label.config(font=("Courier", 11))
    shown_word_label.grid(row='1')

    user_input.set("")


def check_word(_):
    """
    Checks if the word entered is correct
    Adds to score if correct, and to fails if wrong.
    :return:
    """

    global score, fails
    # Check if word is correct and adds 1 to score
    if shown_word.get() == user_input.get():
        score += 1
        display_word()
    # Adds a fail
    else:
        fails += 1
        display_word()


def calc_wpm():
    """
    Calculates words per minute
    :return:
    """
    if score > 0:
        wpm.set(score * 2)
    else:
        return 0


def calc_acc():
    """
    Calculates users typing accuracy
    :return:
    """
    if score > 0:
        accuracy.set(round((score / (fails + score)) * 100, 2))
    else:
        return 0


user_input = StringVar()
shown_word = StringVar()

wpm = IntVar()
accuracy = IntVar()

welcome_text = Label(window, text="""This game is to test your typing skills and help you improve,
click anywhere to begin.""")

welcome_text.config(font=("Courier", 11))
welcome_text.grid()

wpm_label = Label(window, text=wpm.get())
accuracy_label = Label(window, text=accuracy.get())

wpm_text_label = Label(window, text="Your wpm is...")
accuracy_tex_label = Label(window, text="Your accuracy is...")

countdown_label = tk.Label(window)
full_countdown_label = tk.Label(window)

window.bind("<Button-1>", mouse_clicked)
window.bind("<Return>", check_word)

done_label = Label(window, text="Done")
replay_label = Label(window, text="Click anywhere to play again")
results_label = Label(window, text="Your results")

enter_box = Entry(window, textvariable=user_input)
shown_word_label = Label(window, text=shown_word.get())

window.mainloop()
