# math_service/main.py

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Math service is running 🚀"}


@app.get("/pow")
async def power(x: float, y: float):
    return {"operation": "power", "x": x, "y": y, "result": x ** y}


@app.get("/fib")
async def fibonacci(n: int):
    if n < 0:
        return {"error": "n must be >= 0"}
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return {"operation": "fibonacci", "n": n, "result": a}


@app.get("/factorial")
async def factorial(n: int):
    if n < 0:
        return {"error": "n must be >= 0"}
    result = 1
    for i in range(2, n + 1):
        result *= i
    return {"operation": "factorial", "n": n, "result": result}
