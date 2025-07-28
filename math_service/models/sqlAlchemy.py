from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base


class MathRequest(Base):
    __tablename__ = "math_requests"

    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, index=True)
    input_data = Column(String)
    result = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
