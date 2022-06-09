# This is reproduction and extension of https://github.com/lukemcraig/NegativeHarmonizer
# Original written by Luke M Craig.
#
# I have not found a license for the original work, but I have asked for one:
# https://github.com/lukemcraig/NegativeHarmonizer/issues/7
#
# However, in over two years I have not seen a response, so I am
# copying this code here in good faith that the intention of
# publishing this code to github was done for the purpose of sharing
# it freely. Many thanks Luke!

import json
import mido
import uuid
import re
import os
import datetime
import io

from .midi import midi_keys


def get_mirror_axis(tonic):
    return tonic + 3.5


def mirror_note_over_axis(note, axis):
    original_note_distance = axis - note
    return int(axis + original_note_distance)


def find_average_octave_of_tracks(mid):
    octaves = {}
    for i, track in enumerate(mid.tracks):
        track_avg_notes = []
        for message in track:
            if message.type == "note_on":
                track_avg_notes.append(message.note)
        if len(track_avg_notes) > 0:
            track_avg_note = sum(track_avg_notes) / len(track_avg_notes)
            octaves[i] = track_avg_note
            try:
                track_name = track.name
            except AttributeError:
                track_name = i
                print(track_name, track_avg_note)
    return octaves


def mirror_all_notes(mid, mirror_axis, ignored_channels):
    for track in mid.tracks:
        for message in track:
            if message.type == "note_on" or message.type == "note_off":
                if message.channel not in ignored_channels:
                    mirrored_note = mirror_note_over_axis(message.note, mirror_axis)
                    message.note = mirrored_note
    return


def transpose_back_to_original_octaves(
    mid, original_octaves, new_octaves, ignored_channels
):
    for i, track in enumerate(mid.tracks):
        if i in original_octaves:
            notes_distance = original_octaves[i] - new_octaves[i]
            octaves_to_transpose = round(notes_distance / 12)
            for message in track:
                if message.type == "note_on" or message.type == "note_off":
                    if message.channel not in ignored_channels:
                        transposed_note = message.note + (octaves_to_transpose * 12)
                        message.note = int(transposed_note)


def invert_tonality(mid, tonic, ignored_channels, adjust_octaves):
    mirror_axis = get_mirror_axis(tonic)

    if adjust_octaves:
        print("---")
        print("original average note values:")
        original_octaves = find_average_octave_of_tracks(mid)

    mirror_all_notes(mid, mirror_axis, ignored_channels)

    if adjust_octaves:
        print("---")
        print("new average note values:")
        new_octaves = find_average_octave_of_tracks(mid)

        transpose_back_to_original_octaves(
            mid, original_octaves, new_octaves, ignored_channels
        )

        print("---")
        print("adjusted average note values:")
        find_average_octave_of_tracks(mid)
    return


def negative_harmonizer(
    input_file, mirror_positions, ignored_channels=[9], adjust_octaves=False
):
    # Apply repeated inversions to each specified tonic in series:
    positions = re.split("[ \n]+", mirror_positions.strip())
    try:
        tonics = [midi_keys[p] for p in positions]
    except KeyError:
        raise AssertionError(
            f"Mirror positions contain invalid keys: {mirror_positions}"
        )
    for tonic in tonics:
        in_midi = mido.MidiFile(file=input_file)
        invert_tonality(in_midi, tonic, ignored_channels, adjust_octaves)
        out_midi = io.BytesIO()
        in_midi.save(file=out_midi)
        out_midi.seek(0)
        input_file = out_midi
    yield from out_midi
