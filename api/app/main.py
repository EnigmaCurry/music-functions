from typing import Union
from fastapi import FastAPI, Form, UploadFile
from fastapi.responses import Response, StreamingResponse
from pychord import Chord, ChordProgression

from .chords import parse_progression, progression_to_midi
from .negative_harmony import negative_harmonizer

app = FastAPI()


@app.get("/api")
def read_root():
    return {"Hello": "World"}


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


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
