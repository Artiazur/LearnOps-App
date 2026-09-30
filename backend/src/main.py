# Creates and configures the FastAPI application.
#
# This module acts as the application's composition root, where API routers,
# middleware, and global exception handlers are registered. Feature-specific
# business logic remains in their respective modules, while this entry point
# assembles the application's components and infrastructure together.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis
from contextlib import asynccontextmanager
from backend.src.core.config import settings
from backend.src.modules.user.api.user_routers import router as user_router
from backend.src.modules.auth.api.auth_routers import router as auth_router
from backend.src.shared.handlers.error_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True
    )
    
    yield
    
    await app.state.redis.aclose()


# Create the main FastAPI application instance.
app = FastAPI(lifespan=lifespan)


# Register the routers provided by the application's feature modules.
app.include_router(user_router)
app.include_router(auth_router)


# Configure cross-origin requests for the frontend application.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

