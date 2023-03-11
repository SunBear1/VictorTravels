import uvicorn
from fastapi import FastAPI, APIRouter

from users.endpoints import router as users_router

app = FastAPI()

api_router = APIRouter()

app.include_router(users_router, tags=["Endpoints for user operations"])
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
