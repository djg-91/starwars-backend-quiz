from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, HttpUrl


class Planet(BaseModel):
    name: str
    rotation_period: int | None
    orbital_period: int | None
    diameter: int | None
    climate: str | None
    gravity: Any
    terrain: str | None
    surface_water: float | None
    population: int | None
    residents: list[HttpUrl]
    films: list[HttpUrl]
    created: datetime
    edited: datetime
    url: HttpUrl


class PaginatedPlanets(BaseModel):
    count: int
    page: int
    results_count: int
    results: list[Planet]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "count": 59,
                "page": 1,
                "results_count": 1,
                "results": [
                    {
                        "name": "Dantooine",
                        "rotation_period": 25,
                        "orbital_period": 378,
                        "diameter": 9830,
                        "climate": "temperate",
                        "gravity": "1 standard",
                        "terrain": "oceans savannas mountains grasslands",
                        "surface_water": None,
                        "population": 1000,
                        "residents": [],
                        "films": [],
                        "created": "2014-12-10T17:23:29.896000Z",
                        "edited": "2014-12-20T20:58:18.461000Z",
                        "url": "https://swapi.info/api/planets/25"
                    }
                ]
            }
        }
    )
