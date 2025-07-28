

from pydantic import BaseModel
from datetime import datetime


class MathRequestBase(BaseModel):
    operation: str
    input_data: str
    result: float


class MathRequestCreate(MathRequestBase):
    pass


class MathRequestRead(MathRequestBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
