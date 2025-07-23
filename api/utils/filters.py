from datetime import datetime
from typing import Any, get_origin

from fastapi import HTTPException
from pydantic import BaseModel

from api.models import Person, Planet
from shared.logger import get_logger

logger = get_logger('api')


def normalize_value(value: Any) -> Any:
    """
    Normalize a single SWAPI value by:
    - Converting placeholders like 'unknown', 'n/a', 'none' to None.
    - Attempting to parse integers, floats, or ISO datetime strings.
    - Returning a stripped string fallback.
    """
    if isinstance(value, str):
        if value.strip().lower() in {'unknown', 'n/a', 'none'}:
            return None

        stripped = value.replace(',', '').strip()

        for caster in (int, float, try_parse_date):
            try:
                return caster(stripped)
            except (ValueError, TypeError):
                continue

        return stripped

    return value


def normalize_swapi_data(item: dict) -> dict | None:
    """
    Normalize a SWAPI object by cleaning and casting values.

    Skips entries without a 'name' field, as these are incomplete (e.g. /planets/28).

    Args:
        item (dict): Original SWAPI item.

    Returns:
        dict | None: Cleaned item or None if invalid.
    """
    cleaned = {k: normalize_value(v) for k, v in item.items()}

    if cleaned.get('name') is None:
        return None

    return cleaned


def is_sortable_field(model_class: type[BaseModel], field: str) -> bool:
    """
    Determine whether a field can be sorted.

    Args:
        model_class (type[BaseModel]): The Pydantic model (e.g., Person or Planet)
        field (str): Field name to check.

    Returns:
        bool: True if sortable, False otherwise.
    """
    field_info = model_class.model_fields.get(field)
    return field_info is not None and get_origin(field_info.annotation) is not list


def try_parse_date(value: str) -> datetime:
    """
    Try to parse an ISO datetime string, replacing 'Z' with UTC format.

    Args:
        value (str): Date string.

    Returns:
        datetime: Parsed datetime object.
    """
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def sort_key(model: BaseModel, attr: str) -> tuple[int, Any]:
    """
    Generate a sort key for optional values.
    None values are sorted last.

    Args:
        model (BaseModel): The data item.
        attr (str): Attribute name.

    Returns:
        tuple: Sorting key.
    """
    value = getattr(model, attr, None)
    return (1, '') if value is None else (0, value)


def apply_filters_and_sorting(
    model_class: type[BaseModel],
    data: list[Person] | list[Planet],
    search: str | None = None,
    sort_by: str | None = None,
    order: str = 'asc',
) -> list[Person] | list[Planet]:
    """
    Apply filtering by name and optional sorting to the dataset.

    Args:
        model_class (type[BaseModel]): The Pydantic model (e.g., Person or Planet)
        data (list): List of cleaned model instances.
        search (str): optional name-based filter.
        sort_by (str): optional attribute to sort by.
        order (str): asc or desc (default asc).

    Returns:
        list: Filtered and optionally sorted data.
    """
    if search:
        data = [item for item in data if search.lower() in item.name.lower()]

    if sort_by:
        if not is_sortable_field(model_class, sort_by):
            raise HTTPException(status_code=400, detail=f"Cannot sort by '{sort_by}'")

        try:
            data.sort(
                key=lambda x: sort_key(x, sort_by),
                reverse=(order == 'desc'),
            )
        except Exception as e:
            logger.warning(f"Failed to sort by '{sort_by}': {e}")

    return data
