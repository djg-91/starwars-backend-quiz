import httpx
from decouple import config as env
from pydantic import BaseModel

from api.models import Person, Planet
from api.utils.filters import normalize_swapi_data
from shared.logger import get_logger

logger = get_logger('api')


async def fetch_swapi_data(model_class: type[BaseModel], resource: str) -> list[Person | Planet]:
    """
    Fetch and normalize data from the SWAPI for a given resource.

    Args:
        model_class (type[BaseModel]): The Pydantic model (e.g., Person or Planet)
        resource (str): The SWAPI resource endpoint name (e.g., people, planets)

    Returns:
        list[Person] | list[Planet]: List of parsed and validated model instances.

    Raises:
        httpx.HTTPError: If the HTTP request fails or returns an error status.
    """
    url = f'{env("SWAPI_BASE_URL")}/{resource}'

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

            raw_data: list[dict] = response.json()
            # Normalize data (strip 'unknown', cast numbers/dates, etc.)
            normalized_data = list(filter(None, map(normalize_swapi_data, raw_data)))
            # Parse into Pydantic model instances
            return [model_class(**item) for item in normalized_data]

    except httpx.HTTPError:
        logger.exception(f"Failed to fetch '{resource}' from SWAPI: {url}")
        raise
