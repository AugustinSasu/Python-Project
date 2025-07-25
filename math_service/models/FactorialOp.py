

from math_service.models.MathOperation import MathOperation


class FactorialOp(MathOperation):
    n: float

    @property
    def result(self) -> float:
        pass
