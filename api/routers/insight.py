from fastapi import APIRouter, Query, HTTPException
from typing import Literal
from random import choice

router = APIRouter()


@router.get("/simulate-ai-insight")
async def simulate_ai_insight(
    type: Literal["person", "planet"] = Query(..., description="Entity type: person or planet"),
    name: str = Query(..., min_length=1, description="Name of the person or planet"),
):
    """
    Returns a mock AI-generated insight based on the type and name provided.
    """
    if type == "person":
        templates = [
            f"{name} is a pivotal figure whose legacy shapes the galaxy's destiny.",
            f"{name} exhibits extraordinary resilience in the face of galactic turmoil.",
            f"{name}'s journey reflects the classic hero's arc, full of trials and growth.",
        ]
    elif type == "planet":
        templates = [
            f"{name} is known for its unique climate and vital strategic importance.",
            f"The diverse ecosystems of {name} make it a hub for galactic biodiversity.",
            f"{name} has long been a cultural and political center in the outer rim.",
        ]
    else:
        raise HTTPException(status_code=400, detail="Invalid type. Must be 'person' or 'planet'.")

    return {
        "type": type,
        "name": name,
        "insight": choice(templates)
    }
