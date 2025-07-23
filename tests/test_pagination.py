import pytest
from pydantic import BaseModel

from api.utils.pagination import get_filtered_paginated_data


class DummyPerson(BaseModel):
    name: str


MOCK_DATA = [
    {'name': 'Luke'},
    {'name': 'Leia'},
    {'name': 'Anakin'},
    {'name': 'Obi-Wan'},
    {'name': 'Han'},
]


@pytest.mark.asyncio
async def test_pagination_basic(monkeypatch):
    async def mock_fetch(*args, **kwargs):
        return [DummyPerson(**item) for item in MOCK_DATA]

    monkeypatch.setattr('api.utils.pagination.fetch_swapi_data', mock_fetch)

    result = await get_filtered_paginated_data(
        model_class=DummyPerson,
        resource='people',
        page=1,
        page_size=2,
        search=None,
        sort_by=None,
        order='asc',
    )

    assert result['count'] == 5
    assert result['page'] == 1
    assert result['results_count'] == 2
    assert result['results'][0].name == 'Luke'
