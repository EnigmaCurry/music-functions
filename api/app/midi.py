all_keys = (
    "Ab",
    "A",
    "Bb",
    "B",
    "C",
    "C#",
    "Db",
    "D",
    "D#",
    "Eb",
    "E",
    "F",
    "F#",
    "Gb",
    "G",
    "G#",
)


def calculate_midi_keys():
    midi_key_base = {"C": 12, "D": 14, "E": 16, "F": 17, "G": 19, "A": 21, "B": 23}
    midi_keys = {}
    for octave in range(-2, 8):
        for b in midi_key_base.keys():
            key = midi_key_base[b] + (octave * 12)
            if f"{b}b" in all_keys:
                midi_keys[f"{b}b{octave}"] = key - 1
            midi_keys[f"{b}{octave}"] = key
            if f"{b}#" in all_keys:
                midi_keys[f"{b}#{octave}"] = key + 1
    return midi_keys


midi_keys = calculate_midi_keys()
