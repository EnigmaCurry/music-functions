import re
import subprocess
import os
from typing import Union
from fastapi import FastAPI, Form, UploadFile, HTTPException, Request
from fastapi.responses import Response, StreamingResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pychord import Chord, ChordProgression
from pychord.constants import NOTE_VAL_DICT
import isobar as iso

from .midi import all_keys, midi_keys
from .chords import parse_progression, progression_to_midi
from .negative_harmony import negative_harmonizer
from .isobar_util import prepare_midi_timeline, finalize_midi_timeline
from .lsystems import PLSystem

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


def midi_response(midi: bytes, filename: str):
    return Response(
        content=midi,
        media_type="audio/midi",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


class APIError(HTTPException):
    def __init__(self, error):
        super().__init__(400, f"error: {error}")


@app.get("/api/chords/sequence")
@limiter.limit("5/minute")
def chord_sequence(request: Request, chords: str):
    progression, lengths, name = parse_progression(chords)
    midi = progression_to_midi(progression, lengths)
    return midi_response(midi, f"{name}.mid")


@app.post("/api/negative-harmony")
@limiter.limit("5/minute")
def negative_harmony(
    request: Request,
    midi: UploadFile,
    tonics: str = Form(),
    adjust_octaves: bool = Form(False),
):
    return midi_response(
        negative_harmonizer(
            input_file=midi.file, mirror_positions=tonics, adjust_octaves=adjust_octaves
        ),
        "negative_harmony.mid",
    )


@app.get("/api/every-beat")
@limiter.limit("5/minute")
def every_beat(request: Request, start: int = 0, num_bars: int = 16):
    if start >= 2**64:
        raise APIError("start must be <= 2^64")
    if num_bars > 256:
        raise APIError("num_bars must be <= 256")
    filename = f"{start}_{num_bars}bars_every_beat.mid"
    path = f"/tmp/{filename}"
    proc = subprocess.Popen(
        [
            "every_beat",
            "--start",
            str(start),
            "--bars",
            str(num_bars),
            path,
        ]
    )
    proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError(f"every_beat returned {proc.returncode}")
    try:
        with open(path, "rb") as f:
            midi = f.read()
    finally:
        os.remove(path)
    return midi_response(midi, filename)


@app.get("/api/timeline/test")
@limiter.limit("5/minute")
def timeline_test(request: Request):
    timeline, filename, output = midi_timeline = prepare_midi_timeline()
    key = iso.Key("C", "major")
    timeline.schedule(
        {
            "note": iso.PDegree(iso.PSequence([0, 1, 2, 4], 4), key),
            "octave": 5,
            "gate": iso.PSequence([0.5, 1, 2, 1]),
            "amplitude": iso.PSequence([100, 80, 60, 40], 4),
            "duration": 1.0,
        }
    )
    timeline.schedule(
        {
            "note": iso.PDegree(iso.PSequence([7, 6, 4, 2], 4), key),
            "octave": 6,
            "gate": 1,
            "amplitude": iso.PSequence([80, 70, 60, 50], 4),
            "duration": 1.0,
        },
        delay=0.5,
    )
    midi = finalize_midi_timeline(midi_timeline)
    return midi_response(midi, "timeline-test.mid")


lsystem_rule_re = re.compile(r"^[N_\-\+\[\]\?q]+$")


@app.get("/api/melody/lsystem")
@limiter.limit("5/minute")
def timeline_lsystem(
    request: Request, rule: str, root: str, scale: str, octaves: int = 3
):
    raise NotImplementedError("Not ready yet")
    if not lsystem_rule_re.match(rule):
        raise APIError("lsystem rule is invalid")

    rule = rule.replace("q", "?")
    if root not in all_keys:
        raise APIError("invalid root key")
    try:
        scale = iso.Scale.byname(scale)
    except iso.UnknownScaleName:
        raise APIError("Invalid scale name")

    timeline, filename, output = midi_timeline = prepare_midi_timeline()

    notes = PLSystem(rule, depth=4)
    notes = iso.PDegree(notes, scale)
    notes = notes % (12 * octaves) + 60 - int(0.5 * 12 * octaves) + NOTE_VAL_DICT[root]
    timeline.schedule({"note": notes, "duration": 0.25})

    midi = finalize_midi_timeline(midi_timeline)
    return midi_response(midi, f"{rule.replace('?','q')}_{scale.name}.mid")


@app.get("/api/info/scale_names")
def isobar_scales(request: Request):
    return {"scales": [s.name for s in iso.Scale.all()]}


chord_strip_length_re = re.compile("^[0-9]+")


@app.get("/api/info/chord")
def chord_info(request: Request, chord: str):
    try:
        # Strip optional length prefix:
        chord = chord_strip_length_re.sub("", chord)
        chord = Chord(chord)
        quality_name = chord.quality.quality
    except ValueError as e:
        raise APIError("Invalid chord")
    return {
        "chord": chord.chord,
        "valid": True,
        "components": chord.components(),
        "components_with_pitch": chord.components_with_pitch(4),
        "components_midi": [midi_keys[c] for c in chord.components_with_pitch(4)],
        "on": chord.on,
        "root": chord.root,
        "quality": chord.quality.quality,
        "quality_components": chord.quality.components,
    }
