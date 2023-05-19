import random
import streamlit as st
from streamlit import components
from IPython.display import Audio

# Define the available scales with corresponding MIDI program numbers
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

# Global variables
current_scale_type = None
current_tempo = 150


def get_selected_scales():
    selected_scales = []
    for (scale_group, scale_type), checkbox_value in checkbox_values.items():
        if checkbox_value:
            selected_scales.append((scale_group, scale_type))
    return selected_scales


def get_random_scale():
    # Get a random scale from the selected scales
    selected_scales = get_selected_scales()
    if not selected_scales:
        return None
    return random.choice(selected_scales)


def get_scale_notes(scale_type):
    # Get the scale notes based on the scale type
    scale_group, scale = scale_type
    scale_notes = [60 + note for note in scales[scale_group][scale]]
    scale_notes.append(scale_notes[0] + 12)  # Add the root note one octave higher
    return scale_notes


def play_scale(scale_type):
    global current_scale_type, current_tempo

    # Generate the scale notes
    scale_notes = get_scale_notes(scale_type)

    # Calculate the duration based on the tempo
    duration = int(60000 / current_tempo)

    # Play the scale
    audio_elements = []
    for note in scale_notes:
        audio_element = Audio(data=None, url=f"https://path-to-your-audio-files/note_{note}.wav", autoplay=True)
        audio_elements.append(audio_element)

        # Delay between notes
        st.experimental_rerun()

    # Display the audio elements
    for audio_element in audio_elements:
        components.v1.html(audio_element._repr_html_(), height=0)

    # Update the current scale type
    current_scale_type = scale_type


def repeat_scale():
    # Repeat the scale
    if current_scale_type:
        play_scale(current_scale_type)


def check_answer(scale_type):
    if current_scale_type == scale_type:
        st.write("Correct!")
    else:
        st.write("Wrong! Try again.")
        repeat_button.button("Repeat Scale")


def play_random_scale():
    st.empty()  # Clear the answer text

    scale_type = get_random_scale()
    if scale_type:
        play_scale(scale_type)
        repeat_button.button("Repeat Scale")
        for button in scale_buttons.values():
            button.button(button.label)

        st.experimental_rerun()
    else:
        st.write("No scales selected.")


# Create the "Play Random Scale" button
play_button = st.button("Play Random Scale", key="play_button")

# Create the "Repeat Scale" button
repeat_button = st.empty()

# Create the scale groups
checkbox_values = {}
scale_buttons = {}

for scale_group, scales_dict in scales.items():
    st.subheader(scale_group)

    for scale_type in scales_dict.keys():
        checkbox_value = st.checkbox(scale_type, value=False)
        checkbox_values[(scale_group, scale_type)] = checkbox_value

        button = st.empty()
        scale_buttons[(scale_group, scale_type)] = button

# Handle button clicks
if play_button:
    play_random_scale()

for (scale_group, scale_type), button in scale_buttons.items():
    if button.button_clicked():
        check_answer((scale_group, scale_type))
