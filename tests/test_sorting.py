from api.utils.filters import apply_filters_and_sorting
from pydantic import BaseModel

class DummyPerson(BaseModel):
    name: str
    mass: int

def test_sort_by_mass():
    data = [
        DummyPerson(name="A", mass=90),
        DummyPerson(name="B", mass=70),
        DummyPerson(name="C", mass=100),
    ]

    sorted_data = apply_filters_and_sorting(
        DummyPerson,
        data,
        sort_by="mass",
        order="asc"
    )

    masses = [p.mass for p in sorted_data]
    assert masses == [70, 90, 100]
