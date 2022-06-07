import re
import io
from operator import attrgetter
import pretty_midi
from pychord import Chord, ChordProgression

chord_re = re.compile(r"^([0-9]+)?(.*)")


class ChordSyntaxError(Exception):
    pass


def parse_progression(chords):
    seq = re.split("[_ ]", chords.strip())
    chords = []
    lengths = []
    for item in seq:
        try:
            length, chord = chord_re.match(item).groups()
        except TypeError:
            raise ChordSyntaxError(f"Invalid chord: {item}")
        chords.append(chord)
        if length is None:
            lengths.append(4)
        else:
            lengths.append(int(length))
    return (ChordProgression(chords), lengths)


def progression_to_midi(progression, lengths=[]):
    midi_data = pretty_midi.PrettyMIDI()
    piano_program = pretty_midi.instrument_name_to_program("Acoustic Grand Piano")
    piano = pretty_midi.Instrument(program=piano_program)
    position = 0
    for n, chord in enumerate(progression):
        try:
            length = lengths[n] / 4
        except IndexError:
            length = 1
        for note_name in chord.components_with_pitch(root_pitch=4):
            note_number = pretty_midi.note_name_to_number(note_name)
            note = pretty_midi.Note(
                velocity=100, pitch=note_number, start=position, end=position + length
            )
            piano.notes.append(note)
        position += length
    f = io.BytesIO()
    midi_data.instruments.append(piano)
    midi_data.write(f)
    out = f.getvalue()
    f.close()
    return out
