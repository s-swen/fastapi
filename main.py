from fastapi import FastAPI, HTTPException
from schemas import GenreURLChoices, Band


app = FastAPI()

BANDS = [
    {'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
    {'id': 2, 'name': 'Aphex Twin', 'genre': 'Electronic'},
    {'id': 3, 'name': 'Black Sabbath', 'genre': 'Metal'},
    {'id': 4, 'name': 'Wu-Tang Clan', 'genre': 'Hip-Hop'},
]

@app.get('/bands')
async def bands() -> list[Band]:
    return [
        Band(**band) for band in BANDS
    ]

@app.get('/bands/{band_id}')
async def band(band_id: int) -> Band:
    band = next((Band(**band) for band in BANDS if band['id'] == band_id), None)
    if not band:
        raise HTTPException(status_code=404, detail="band not found")
    return band

@app.get('/bands/genre/{genre}')
async def genre(genre: GenreURLChoices) -> list[Band]:
    return [
        Band(**band) for band in BANDS if band['genre'].lower() == genre.value
    ]