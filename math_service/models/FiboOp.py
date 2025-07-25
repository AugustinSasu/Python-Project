

from math_service.models.MathOperation import MathOperation


class FibonacciOp(MathOperation):
    n: float

    @property
    def result(self) -> float:
        pass
