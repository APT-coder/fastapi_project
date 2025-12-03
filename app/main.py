from fastapi import FastAPI
from app.routers import auth, permissions, roles, users, items

app = FastAPI(title="my_fastapi_project_async")

@app.on_event("startup")
async def startup():
    # If needed (Alembic recommended instead)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.create_all)
    pass

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(permissions.router, prefix="/permissions", tags=["Permissions"])
app.include_router(roles.router, prefix="/roles", tags=["Roles"])
app.include_router(items.router, prefix="/items", tags=["items"])

@app.get("/")
async def root():
    return {"message": "Async FastAPI working!"}
