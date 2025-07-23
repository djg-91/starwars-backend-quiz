from fastapi import FastAPI

from api.routers import insight, people, planets

app = FastAPI(title='Star Wars API')

app.include_router(people.router, prefix='/people', tags=['People'])
app.include_router(planets.router, prefix='/planets', tags=['Planets'])
app.include_router(insight.router, tags=["AI Insight"])
