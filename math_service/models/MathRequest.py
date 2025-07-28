

from pydantic import BaseModel
from datetime import datetime


class MathRequestBase(BaseModel):
    operation: str
    input_data: str


class MathRequestCreate(MathRequestBase):
    pass


class MathRequestRead(MathRequestBase):
    id: int
    timestamp: datetime
    result: float

    model_config = {
        "from_attributes": True
    }
