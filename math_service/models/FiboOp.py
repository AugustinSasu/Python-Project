

from models.MathOperation import MathOperation


class FibonacciOp(MathOperation):
    n: float

    @property
    def result(self) -> float:
        n_int = int(self.n)
        if n_int <= 0:
            return 0.0
        elif n_int == 1:
            return 1.0

        a, b = 0, 1
        for _ in range(2, n_int + 1):
            a, b = b, a + b
        return float(b)
