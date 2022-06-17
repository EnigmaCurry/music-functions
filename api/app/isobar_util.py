import os
from collections import namedtuple
import tempfile
import isobar as iso
from isobar.io import MidiFileOutputDevice

MidiTimeline = namedtuple("MidiTimeline", ("timeline", "filename", "output"))


def prepare_midi_timeline():
    filename = tempfile.mktemp()
    output = MidiFileOutputDevice(filename)
    timeline = iso.Timeline(iso.MAX_CLOCK_RATE, output_device=output)
    timeline.stop_when_done = True
    return MidiTimeline(timeline, filename, output)


def finalize_midi_timeline(timeline: MidiTimeline):
    timeline.timeline.run()
    timeline.output.write()
    with open(timeline.filename, "rb") as f:
        midi = f.read()
        os.remove(timeline.filename)
    return midi
