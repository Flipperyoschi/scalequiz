import random
import streamlit as st
import pygame
import pygame.midi

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

# Set the desired MIDI output device name
output_device_name = "Microsoft MIDI Mapper"

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

    # Initialize Pygame MIDI
    pygame.midi.init()

    # Find the desired output device ID by name
    device_id = None
    num_devices = pygame.midi.get_count()
    for i in range(num_devices):
        device_info = pygame.midi.get_device_info(i)
        device_name = device_info[1].decode("utf-8")
        if device_name == output_device_name:
            device_id = i
            break

    if device_id is None:
        st.error("Output device not found: " + output_device_name)
        return

    # Open the specified output device
    output = pygame.midi.Output(device_id)

    # Set the instrument/program
    output.set_instrument(0)

    # Calculate the duration based on the tempo
    duration = int(60000 / current_tempo)

    # Play the scale
    for note in scale_notes:
        output.note_on(note, velocity=127)
        pygame.time.wait(duration)
        output.note_off(note)

    # Close the MIDI output device
    output.close()

    # Quit Pygame MIDI
    pygame.midi.quit()

    # Update the current scale type
    current_scale_type = scale_type


def repeat_scale():
    # Repeat the scale
    if current_scale_type:
        play_scale(current_scale_type)


def check_answer(scale_type):
    if current_scale_type == scale_type:
        st.success("Correct!")
    else:
        st.error("Wrong! Try again.")
        repeat_scale()


def play_random_scale():
    # Clear the answer text
    st.empty()

    scale_type = get_random_scale()
    if scale_type:
        play_scale(scale_type)
        repeat_button.button("Repeat Scale")
        for button in scale_buttons.values():
            button.button(button.label)

        # Schedule clearing the answer text after 3 seconds
        st.empty()
    else:
        st.warning("No scales selected.")


# Create the "Play Random Scale" button
play_button = st.button("Play Random Scale", on_click=play_random_scale)

# Create the "Repeat Scale" button
repeat_button = st.button("Repeat Scale", on_click=repeat_scale, state="disabled")

# Create the scale groups
checkbox_values = {}
scale_buttons = {}

for scale_group, scales_dict in scales.items():
    st.subheader(scale_group)
    for scale_type in scales_dict.keys():
        checkbox_values[(scale_group, scale_type)] = st.checkbox(scale_type)
        button = st.button(scale_type, on_click=lambda st=(scale_group, scale_type): check_answer(st))
        scale_buttons[(scale_group, scale_type)] = button

# Create the feedback section
st.subheader("Feedback")
feedback_text = st.empty()

# Create the tempo slider
current_tempo = st.slider("Tempo", min_value=100, max_value=400, value=current_tempo)

# Start the Streamlit app
if __name__ == "__main__":
    play_random_scale()
