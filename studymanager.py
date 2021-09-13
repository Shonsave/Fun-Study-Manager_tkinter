import tkinter as tk
from tkinter.ttk import *
import datetime
import winsound
from PIL import Image, ImageTk
import cx_Freeze
import sys

root = tk.Tk()
root.geometry("980x600")
root.title("Study Manager")
root.iconbitmap('StudyIntervalsIcon.ico')

root.columnconfigure(0, weight=1)

start_button_frame = Frame(root)
start_button_frame.columnconfigure(1, weight=1)
start_button_frame.grid(row=5, column=0)

selector_frame = Frame(root)
selector_frame.columnconfigure(1, weight=1)
selector_frame.grid(row=2, column=0)

title_label = Label(root, text="Study Monitor".upper(), font=("Helvetica", 30, "bold underline"))
title_label.grid(row=0, column=0, pady=(30, 5))
logo = ImageTk.PhotoImage(Image.open('StudyIntervalsLogo.png').resize((100, 100), Image.ANTIALIAS))
logo_label = Label(image=logo)
logo_label.grid(row=1, column=0, pady=(0, 20))

study_intervals = ['10', '15', '20', '30', '45', '60']
break_intervals = ['2', '5', '7', '10', '15', '20']

study_time_sv = tk.StringVar(root)
study_time_sv.set(study_intervals[3])
break_time_sv = tk.StringVar(root)
break_time_sv.set(break_intervals[2])

global study_time
global break_time
study_time = int(study_time_sv.get()) * 60
break_time = int(break_time_sv.get()) * 60

global time_left
time_left = study_time
global total_study_time_elapsed
total_study_time_elapsed = 0

global current_interval_type
current_interval_type = 's'

global study_ongoing
study_ongoing = False
global was_study
was_study = False


def reset_studies(choice):
    global study_time
    global break_time
    study_time = int(study_time_sv.get()) * 60
    break_time = int(break_time_sv.get()) * 60

    global time_left
    time_left = study_time
    global current_interval_type
    current_interval_type = 's'

    global study_ongoing
    study_ongoing = False
    global was_study
    was_study = False


study_label = Label(selector_frame, text="Select length of one study interval(in minutes): ",
                    font=("Cambria", 14, "italic"))
break_label = Label(selector_frame, text="Select length of one break interval(in minutes): ",
                    font=("Cambria", 14, "italic"))
study_label.grid(row=0, column=0)

study_time_select = tk.OptionMenu(selector_frame, study_time_sv, *study_intervals, command=reset_studies)
break_time_select = tk.OptionMenu(selector_frame, break_time_sv, *break_intervals, command=reset_studies)
study_time_select.config(height=2, width=5)
break_time_select.config(height=2, width=5)
study_time_select.grid(row=0, column=1)

break_label.grid(row=1, column=0)
break_time_select.grid(row=1, column=1, padx=10)


def study_manager(int_type: str):
    global study_time
    global break_time
    global study_ongoing
    study_ongoing = True
    global current_interval_type
    current_interval_type = int_type
    global time_left
    if current_interval_type.lower() == 's':
        time_left = study_time
    else:
        time_left = break_time

    do_interval(current_interval_type)


def do_interval(int_type: str):
    if study_ongoing:
        global time_left
        global total_study_time_elapsed

        if time_left > 0:
            time_left -= 1

            if int_type.lower() == 's':
                total_study_time_elapsed += 1

            total_time_elapsed_mins = total_study_time_elapsed // 60
            total_time_elapsed_secs = total_study_time_elapsed % 60

            root.after(1000, lambda: do_interval(int_type))
            time_left_mins = time_left // 60
            time_left_secs = time_left % 60

            if int_type.lower() == 's':
                time_left_label.config(text="Study - time left: " + str(time_left_mins) + ":" + str(time_left_secs))

                total_time_elapsed_label.config(text="Total study time elapsed: " + str(total_time_elapsed_mins) + ":" + str(total_time_elapsed_secs))

            else:
                time_left_label.config(text="Break - time left: " + str(time_left_mins) + ":" + str(time_left_secs))

        else:
            for i in range(3):
                root.after(500, winsound.Beep(2000, 1000))

            if int_type.lower() == 's':
                next_interval = 'b'
            else:
                next_interval = 's'

            study_manager(next_interval)


def terminate_studies():
    global study_ongoing
    study_ongoing = False
    global current_interval_type
    current_interval_type = 's'
    global time_left
    time_left = study_time
    time_left_label.config(text="Time left: 00:00")
    study_time_select.config(state='normal')
    break_time_select.config(state='normal')

    global total_study_time_elapsed
    total_study_time_elapsed = 0


def pause_play_study():
    study_time_select.config(state='disabled')
    break_time_select.config(state='disabled')
    global time_left
    global study_time
    global break_time
    global study_ongoing
    global current_interval_type

    study_time = int(study_time_sv.get()) * 60
    break_time = int(break_time_sv.get()) * 60

    global was_study
    if study_ongoing:
        was_study = True

    study_ongoing = not study_ongoing

    if study_ongoing and not was_study:
        study_manager(current_interval_type)

    if study_ongoing and was_study:
        do_interval(current_interval_type)


time_left_label = tk.Label(root, text='Time left: 00:00', font=("Arial", 22, "bold"))
time_left_label.grid(row=4, column=0, pady=20)

start_pause_button = tk.Button(start_button_frame, text='Start Studies! | Pause', command=pause_play_study, height=3)
terminate_study_button = tk.Button(start_button_frame, text='Terminate Studies... ', command=terminate_studies,
                                   height=3)
start_pause_button.grid(row=0, column=0, padx=10)
terminate_study_button.grid(row=0, column=1, padx=10)

total_time_elapsed_label = tk.Label(root, text='Total study time elapsed: 00:00', font=("Calibri", 16, "italic"))
total_time_elapsed_label.grid(row=6, column=0, pady=(60, 0))

root.mainloop()
