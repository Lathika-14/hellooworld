from fastapi import FastAPI

from app.auth.router import router as auth_router

app = FastAPI(
    title="Food Delivery API"
)

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "Food Delivery API is running"}