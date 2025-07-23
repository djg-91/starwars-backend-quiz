from api.utils.filters import apply_filters_and_sorting
from pydantic import BaseModel

class DummyPerson(BaseModel):
    name: str

def test_search_filter():
    data = [
        DummyPerson(name="Luke Skywalker"),
        DummyPerson(name="Leia Organa"),
        DummyPerson(name="Anakin Skywalker"),
    ]

    filtered = apply_filters_and_sorting(
        DummyPerson,
        data,
        search="sky",
    )

    assert len(filtered) == 2
    assert all("sky" in p.name.lower() for p in filtered)
