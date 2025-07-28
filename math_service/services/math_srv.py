from repos.RequestsRepo import RequestsRepo

from models.PowOp import PowOp
from models.FiboOp import FibonacciOp
from models.FactorialOp import FactorialOp

from models.MathRequest import MathRequestCreate  # Adjust path as needed


class MathService:
    def __init__(self, requests_repo: RequestsRepo):
        self.requests_repo = requests_repo

    async def power(self, x: float, y: float) -> dict:
        pow_op = PowOp(x=x, y=y)
        result = pow_op.result

        request_data = MathRequestCreate(
            operation="power",
            input_data=f'{{"x": {x}, "y": {y}}}',  # store as JSON string
            result=result
        )

        await self.requests_repo.create_request(request_data)

        return result

    async def fibonacci(self, n: int) -> dict:
        if n < 0:
            return {"error": "n must be >= 0"}

        fiboOp = FibonacciOp(n=n)
        result = fiboOp.result

        request_data = MathRequestCreate(
            operation="fibonacci",
            input_data=f'{{"n": {n}}}',  # store as JSON string
            result=result
        )

        await self.requests_repo.create_request(request_data)

        return result

    async def factorial(self, n: int) -> dict:
        if n < 0:
            return {"error": "n must be >= 0"}

        fact_op = FactorialOp(n=n)
        result = fact_op.result

        request_data = MathRequestCreate(
            operation="factorial",
            input_data=f'{{"n": {n}}}',  # store as JSON string
            result=result
        )

        await self.requests_repo.create_request(request_data)

        return result
