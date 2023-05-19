#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
import tkinter as tk
from tkinter import ttk

# Define the available scales
scales = {
    "Church Modes": {
        "Ionian": [0, 2, 4, 5, 7, 9, 11],
        "Dorian": [0, 2, 3, 5, 7, 9, 10],
        "Phrygian": [0, 1, 3, 5, 7, 8, 10],
        "Lydian": [0, 2, 4, 6, 7, 9, 11],
        "Mixolydian": [0, 2, 4, 5, 7, 9, 10],
        "Aeolian": [0, 2, 3, 5, 7, 8, 10],
        "Locrian": [0, 1, 3, 5, 6, 8, 10],
    },
    "Alternative Modes": {
        "Half-diminished": [0, 2, 3, 5, 6, 8, 10],
        "Harmonic minor": [0, 2, 3, 5, 7, 8, 11],
        "Melodic minor": [0, 2, 3, 5, 7, 9, 11],
        "Pentatonic major": [0, 2, 4, 7, 9],
        "Pentatonic minor": [0, 3, 5, 7, 10],
        "Whole-tone scale": [0, 2, 4, 6, 8, 10],
        "Altered scale": [0, 1, 3, 4, 6, 8, 10],
    }
}

current_scale_type = None
current_tempo = 150

def get_selected_scales():
    selected_scales = []
    for (scale_group, scale_type), checkbox_var in checkbox_vars.items():
        if checkbox_var.get() == 1:
            selected_scales.append((scale_group, scale_type))
    return selected_scales

def get_random_scale():
    selected_scales = get_selected_scales()
    if not selected_scales:
        return None
    return random.choice(selected_scales)

def get_scale_notes(scale_type):
    scale_group, scale = scale_type
    scale_notes = [60 + note for note in scales[scale_group][scale]]
    scale_notes.append(scale_notes[0] + 12)
    return scale_notes

def play_scale(scale_type):
    global current_scale_type, current_tempo

    scale_notes = get_scale_notes(scale_type)

    # Replace the code related to MIDI output with your specific online interpreter's MIDI support, if available.
    # You may need to consult the online interpreter's documentation or support resources to understand how to play MIDI.

    # Update the current scale type
    current_scale_type = scale_type

def repeat_scale():
    if current_scale_type:
        play_scale(current_scale_type)

def check_answer(scale_type, button):
    if current_scale_type == scale_type:
        label_text.set("Correct!")
    else:
        label_text.set("Wrong! Try again.")
        repeat_button.configure(state=tk.NORMAL)

def play_random_scale():
    label_text.set("")
    scale_type = get_random_scale()
    if scale_type:
        play_scale(scale_type)
        repeat_button.configure(state=tk.NORMAL)
        for button in scale_buttons.values():
            button.configure(state=tk.NORMAL)
        window.after(3500, clear_answer_text)
    else:
        label_text.set("No scales selected.")

def clear_answer_text():
    label_text.set("")

window = tk.Tk()
window.title("Scale Quiz")
window.geometry("500x600")

play_button = ttk.Button(window, text="Play Random Scale", command=play_random_scale)
play_button.pack(pady=10)

repeat_button = ttk.Button(window, text="Repeat Scale", command=repeat_scale)
repeat_button.pack(pady=5)
repeat_button.configure(state=tk.DISABLED)

scale_group_frame = tk.Frame(window)
scale_group_frame.pack(pady=5, padx=5)

checkbox_vars = {}
scale_buttons = {}

for scale_group, scales_dict in scales.items():
    group_label = ttk.Label(scale_group_frame, text=scale_group)
    group_label.pack(side=tk.LEFT, padx=5)
    group_frame = tk.Frame(scale_group_frame)
    group_frame.pack(side=tk.LEFT, padx=5)

    for scale_type in scales_dict.keys():
        checkbox_var = tk.IntVar()
        checkbox_vars[(scale_group, scale_type)] = checkbox_var
        checkbox = ttk.Checkbutton(group_frame, text=scale_type, variable=checkbox_var)
        checkbox.pack(side=tk.TOP, pady=3)

        button = ttk.Button(group_frame, text=scale_type, command=lambda st=(scale_group, scale_type): check_answer(st, button))
        button.pack(side=tk.TOP, pady=3)
        scale_buttons[(scale_group, scale_type)] = button

label_text = tk.StringVar()
feedback_label = ttk.Label(window, textvariable=label_text)
feedback_label.pack(pady=10)

tempo_frame = tk.Frame(window)
tempo_frame.pack(pady=1)
tempo_label = ttk.Label(tempo_frame, text="Tempo")
tempo_label.pack(side=tk.LEFT, padx=3)
tempo_slider = ttk.Scale(tempo_frame, from_=100, to=400, orient=tk.HORIZONTAL)
tempo_slider.set(current_tempo)
tempo_slider.pack(side=tk.LEFT, padx=3)

current_tempo = tempo_slider.get()

# Replace the window.mainloop() statement with your specific online interpreter's code to start the event loop.
# Consult the documentation or support resources of the online interpreter for the correct syntax.

