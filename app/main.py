from fastapi import FastAPI
from app.db.database import engine, Base
from app.routers import users, items

app = FastAPI(title="my_fastapi_project_async")

@app.on_event("startup")
async def startup():
    # If needed (Alembic recommended instead)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    pass

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(items.router, prefix="/items", tags=["items"])

@app.get("/")
async def root():
    return {"message": "Async FastAPI working!"}
