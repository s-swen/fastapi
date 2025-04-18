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
) -> list[BandWithID]:
    band_list = [BandWithID(**band) for band in BANDS]
    if genre:
        return [
            band for band in band_list if band.genre.value.lower() == genre.value
        ]
    if has_albums:
        return [
            band for band in band_list if band.albums
        ]
    return band_list

@app.get('/bands/{band_id}')
async def band(band_id: int) -> BandWithID:
    band = next((BandWithID(**band) for band in BANDS if band['id'] == band_id), None)
    if not band:
        raise HTTPException(status_code=404, detail="band not found")
    return band

@app.post('/bands')
async def create_band(band_data: BandCreate) -> BandWithID:
    id = BANDS[-1]['id'] + 1
    band = BandWithID(id=id, **band_data.model_dump()).model_dump()
    BANDS.append(band)
    return band