
from contextlib import asynccontextmanager
from broker.publisher import Publisher
import os
from fastapi import FastAPI
from database import engine  # you may or may not still need this depending on your usage
from database import Base
from routes import math_routes
from logging_utils.logging_config import init_logging


publisher = Publisher()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure persistent-db directory exists for SQLite
    os.makedirs("./persistent-db", exist_ok=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Connect to message broker
    await publisher.connect()

    # Inject broker into routes
    math_routes.publisher = publisher

    # Initialize logging
    init_logging(rabbit_host="rabbitmq", rabbit_queue="logs")

    yield  # app runs here

    # Shutdown cleanup
    await engine.dispose()  # optional: if using SQLAlchemy engine elsewhere
    if publisher.connection:
        await publisher.connection.close()


app = FastAPI(lifespan=lifespan)
app.include_router(math_routes.router)
