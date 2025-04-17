from fastapi import FastAPI, HTTPException
from schemas import GenreURLChoices, BandCreate, BandWithID


app = FastAPI()

BANDS = [
    {'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
    {'id': 2, 'name': 'Aphex Twin', 'genre': 'Electronic'},
    {'id': 3, 'name': 'Black Sabbath', 'genre': 'Metal', 'albums': [
        {'title': 'Master of Reality', 'release_date': '1971-07-21'},
        {'title': 'Master of Reality', 'release_date': '1971-07-21'},
    ]},
    {'id': 4, 'name': 'Wu-Tang Clan', 'genre': 'Hip-Hop'},
]

@app.get('/bands')
async def bands(
    genre: GenreURLChoices | None = None,
    has_albums: bool = False
) -> list[Band]:
    band_list = [Band(**band) for band in BANDS]
    if genre:
        return [
            band for band in band_list if band.genre.lower() == genre.value
        ]
    if has_albums:
        return [
            band for band in band_list if band.albums
        ]
    return band_list

@app.get('/bands/{band_id}')
async def band(band_id: int) -> Band:
    band = next((Band(**band) for band in BANDS if band['id'] == band_id), None)
    if not band:
        raise HTTPException(status_code=404, detail="band not found")
    return band

# @app.get('/bands/genre/{genre}')
# async def genre(genre: GenreURLChoices) -> list[Band]:
#     return [
#         Band(**band) for band in BANDS if band['genre'].lower() == genre.value
#     ]