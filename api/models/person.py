from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl


class Person(BaseModel):
    name: str
    height: int | None
    mass: float | None
    hair_color: str | None
    skin_color: str | None
    eye_color: str | None
    birth_year: str | None
    gender: str | None
    homeworld: HttpUrl
    films: list[HttpUrl]
    species: list[HttpUrl]
    vehicles: list[HttpUrl]
    starships: list[HttpUrl]
    created: datetime
    edited: datetime
    url: HttpUrl


class PaginatedPeople(BaseModel):
    count: int
    page: int
    results_count: int
    results: list[Person]

    model_config = ConfigDict(
        json_schema_extra={
            'example': {
                'count': 82,
                'page': 1,
                'results_count': 1,
                'results': [
                    {
                        'name': 'Luke Skywalker',
                        'height': 172,
                        'mass': 77.0,
                        'hair_color': 'blond',
                        'skin_color': 'fair',
                        'eye_color': 'blue',
                        'birth_year': '19BBY',
                        'gender': 'male',
                        'homeworld': 'https://swapi.info/api/planets/1',
                        'films': [
                            'https://swapi.info/api/films/1',
                            'https://swapi.info/api/films/2',
                            'https://swapi.info/api/films/3',
                            'https://swapi.info/api/films/6',
                        ],
                        'species': [],
                        'vehicles': [
                            'https://swapi.info/api/vehicles/14',
                            'https://swapi.info/api/vehicles/30',
                        ],
                        'starships': [
                            'https://swapi.info/api/starships/12',
                            'https://swapi.info/api/starships/22',
                        ],
                        'created': '2014-12-09T13:50:51.644000Z',
                        'edited': '2014-12-20T21:17:56.891000Z',
                        'url': 'https://swapi.info/api/people/1',
                    }
                ],
            }
        }
    )
