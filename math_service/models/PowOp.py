

from models.MathOperation import MathOperation


class PowOp(MathOperation):
    x: float
    y: float

    @property
    def result(self) -> float:
        return self.x ** self.y
