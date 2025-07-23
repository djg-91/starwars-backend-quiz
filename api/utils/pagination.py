from typing import Any

from pydantic import BaseModel

from api.models import Person, Planet
from api.services.swapi_proxy import fetch_swapi_data
from api.utils.filters import apply_filters_and_sorting
from shared.logger import get_logger

logger = get_logger('api')


async def get_filtered_paginated_data(
    model_class: type[BaseModel],
    resource: str,
    page: int,
    page_size: int,
    search: str | None,
    sort_by: str | None,
    order: str | None,
) -> dict[str, Any]:
    """
    Fetch data from SWAPI, apply search/sort filters, and return paginated results.

    Args:
        model_class (type[BaseModel]): the Pydantic model (e.g., Person, Planet).
        resource (str): the SWAPI resource endpoint name (e.g., people, planets).
        page (int): page number (1-based).
        page_size (int): number of results per page.
        search (str): optional name-based filter.
        sort_by (str): optional attribute to sort by.
        order (str): asc or desc (default asc).

    Returns:
        dict[str, Any]: A paginated response dictionary
    """
    logger.info(
        f'GET /{resource} | page={page} page_size={page_size} '
        f'search={search} sort_by={sort_by} order={order}'
    )

    data: list[Person | Planet] = await fetch_swapi_data(model_class, resource)

    filtered_data: list[Person | Planet] = apply_filters_and_sorting(
        model_class, data, search=search, sort_by=sort_by, order=order
    )

    # Manual pagination
    start = (page - 1) * page_size
    end = start + page_size
    paged_data = filtered_data[start:end]

    return {
        'count': len(filtered_data),  # Total after filtering
        'page': page,
        'results_count': len(paged_data),  # Current page size
        'results': paged_data,
    }
