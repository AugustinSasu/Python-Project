

from models.MathOperation import MathOperation


class FactorialOp(MathOperation):
    n: float

    @property
    def result(self) -> float:
        n_int = int(self.n)
        if n_int < 0:
            raise ValueError("Factorial is not defined for negative numbers")

        result = 1
        for i in range(2, n_int + 1):
            result *= i
        return float(result)
