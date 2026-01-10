from fastapi import FastAPI
from app.routers import auth, documents, email, feedback, otp, permissions, products, roles, users

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
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(email.router, prefix="/email", tags=["Email"])
app.include_router(otp.router, prefix="/otp", tags=["OTP"])
app.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])


@app.get("/")
async def root():
    return {"message": "Async FastAPI working!"}
