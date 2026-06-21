from fastapi import FastAPI
from src.modules.user.api.user_routers import router as user_router
from src.modules.auth.api.auth_routers import router as auth_router


app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)

