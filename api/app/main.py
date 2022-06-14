from typing import Union
from fastapi import FastAPI, Form, UploadFile, HTTPException
from fastapi.responses import Response, StreamingResponse, FileResponse
from pychord import Chord, ChordProgression
import subprocess

from .chords import parse_progression, progression_to_midi
from .negative_harmony import negative_harmonizer

app = FastAPI()


@app.get("/api/chords/sequence")
def chord_sequence(chords: str):
    progression, lengths, name = parse_progression(chords)
    midi = progression_to_midi(progression, lengths)
    return Response(
        content=midi,
        media_type="audio/midi",
        headers={"Content-Disposition": f'attachment; filename="{name}.mid"'},
    )


@app.post("/api/negative-harmony")
def negative_harmony(
    midi: UploadFile, tonics: str = Form(), adjust_octaves: bool = Form(False)
):
    return StreamingResponse(
        negative_harmonizer(
            input_file=midi.file, mirror_positions=tonics, adjust_octaves=adjust_octaves
        ),
        media_type="audio/midi",
    )


@app.get("/api/every-beat")
def every_beat(start: int = 0, num_bars: int = 16):
    if start >= 2**64:
        raise HTTPException(400, "start must be <= 2^64")
    if num_bars > 256:
        raise HTTPException(400, "num_bars must be <= 256")
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
    return FileResponse(path, media_type="audio/midi", filename=filename)
