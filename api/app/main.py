from typing import Union
from fastapi import FastAPI
from fastapi.responses import Response
from pychord import Chord, ChordProgression

from .chords import parse_progression, progression_to_midi

app = FastAPI()


@app.get("/api")
def read_root():
    return {"Hello": "World"}


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/api/chords/sequence")
def chord_sequence(chords: str):
    progression, lengths = parse_progression(chords)
    midi = progression_to_midi(progression, lengths)
    return Response(
        content=midi,
        media_type="audio/midi",
        headers={"Content-Disposition": f'attachment; filename="{chords}.mid"'},
    )
