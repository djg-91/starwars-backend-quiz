from fastapi import APIRouter, Query

from api.models.person import PaginatedPeople, Person
from api.utils.pagination import get_filtered_paginated_data

router = APIRouter()


@router.get('/', response_model=PaginatedPeople)
async def get_people(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str | None = None,
    sort_by: str | None = None,
    order: str | None = Query('asc', pattern='^(asc|desc)$'),
):
    """
    Retrieve a paginated list of people.

    Args:
    - **page**: Page number (1-based).
    - **page_size**: Number of results per page (default 10).
    - **search**: Optional name filter.
    - **sort_by**: Optional attribute to sort by.
    - **order**: asc or desc (default asc).
    """
    return await get_filtered_paginated_data(
        model_class=Person,
        resource='people',
        page=page,
        page_size=page_size,
        search=search,
        sort_by=sort_by,
        order=order,
    )
