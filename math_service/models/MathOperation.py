from abc import ABC, abstractmethod
from pydantic import BaseModel


class MathOperation(BaseModel, ABC):
    @property
    @abstractmethod
    def result(self) -> float:
        pass
