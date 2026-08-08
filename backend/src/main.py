from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.src.modules.user.api.user_routers import router as user_router
from backend.src.modules.auth.api.auth_routers import router as auth_router


app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
