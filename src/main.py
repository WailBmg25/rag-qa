from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from routes import base_router, data_router
from helpers import get_settings
from contextlib import asynccontextmanager
from helpers import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.db_client = app.mongo_conn[settings.MONGODB_DB_NAME]
    logger.info("✅ Connected to MongoDB at %s", settings.MONGODB_URL)

    # Yield control to the app (app runs here)
    yield

    # --- Shutdown ---
    app.mongo_conn.close()
    logger.info("🛑 MongoDB connection closed.")

app = FastAPI(lifespan=lifespan)

# Routers
app.include_router(base_router)
app.include_router(data_router)