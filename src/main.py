from fastapi import FastAPI
from src.modules.user.api.user_routers import router as user_router


app = FastAPI()
app.include_router(user_router)
