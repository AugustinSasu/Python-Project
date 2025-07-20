# math_service/main.py

from fastapi import FastAPI

from database import engine
from database import SessionLocal

from models import Base
from models import MathRequest

#pt ca app.on_event("startup") is deprecated in FastAPI 0.100.0 folosim asynccontextmanager
from contextlib import asynccontextmanager


#initialize the database
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP CODE HERE
    async with engine.begin() as conn: # Create a connection to the database
        await conn.run_sync(Base.metadata.create_all) # Create all tables in the database from the Base class which math_service.models.py defines
    yield
    # SHUTDOWN CODE HERE
    await engine.dispose()


import json


# Initialize FastAPI app with lifespan: FastAPI expects a function here to handle startup
app = FastAPI(lifespan = lifespan)


async def log_request(operation: str, inputs: dict, result: float):
    async with SessionLocal() as session:
        math_request = MathRequest(
            operation=operation,
            input_data=json.dumps(inputs),
            result=result
        )
        session.add(math_request)
        await session.commit()


@app.get("/")
async def root():
    return {"message": "Math service is running 🚀"}


@app.get("/pow")
async def power(x: float, y: float):
    result = x ** y
    await log_request("power", {"x": x, "y": y}, result)
    return {"operation": "power", "x": x, "y": y, "result": result}


@app.get("/fib")
async def fibonacci(n: int):
    if n < 0:
        return {"error": "n must be >= 0"}
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    result = a
    await log_request("fibonacci", {"n": n}, result)
    return {"operation": "fibonacci", "n": n, "result": result}


@app.get("/factorial")
async def factorial(n: int):
    if n < 0:
        return {"error": "n must be >= 0"}
    result = 1
    for i in range(2, n + 1):
        result *= i
    await log_request("factorial", {"n": n}, result)
    return {"operation": "factorial", "n": n, "result": result}
