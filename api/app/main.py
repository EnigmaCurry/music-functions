import subprocess
import os
from typing import Union
from fastapi import FastAPI, Form, UploadFile, HTTPException, Request
from fastapi.responses import Response, StreamingResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pychord import Chord, ChordProgression

from .chords import parse_progression, progression_to_midi
from .negative_harmony import negative_harmonizer

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/api/chords/sequence")
@limiter.limit("5/minute")
def chord_sequence(request: Request, chords: str):
    progression, lengths, name = parse_progression(chords)
    midi = progression_to_midi(progression, lengths)
    return Response(
        content=midi,
        media_type="audio/midi",
        headers={"Content-Disposition": f'attachment; filename="{name}.mid"'},
    )


@app.post("/api/negative-harmony")
@limiter.limit("5/minute")
def negative_harmony(
    request: Request,
    midi: UploadFile,
    tonics: str = Form(),
    adjust_octaves: bool = Form(False),
):
    return StreamingResponse(
        negative_harmonizer(
            input_file=midi.file, mirror_positions=tonics, adjust_octaves=adjust_octaves
        ),
        media_type="audio/midi",
    )


@app.get("/api/every-beat")
@limiter.limit("5/minute")
def every_beat(request: Request, start: int = 0, num_bars: int = 16):
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
    try:
        with open(path, "rb") as f:
            midi = f.read()
    finally:
        os.remove(path)
    return Response(
        content=midi,
        media_type="audio/midi",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
