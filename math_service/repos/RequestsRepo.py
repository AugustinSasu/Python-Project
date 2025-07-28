from typing import Optional
from models.MathRequest import MathRequestCreate, MathRequestRead
from models.sqlAlchemy import MathRequest
from sqlalchemy.future import select


class RequestsRepo:
    def __init__(self, db):
        self.db = db

    async def create_request(self, request_data: MathRequestCreate) -> int:
        new_request = MathRequest(**request_data.model_dump())
        self.db.add(new_request)
        await self.db.commit()
        await self.db.refresh(new_request)
        return new_request.id

    async def get_request(self, request_id: int) -> Optional[MathRequestRead]:
        stmt = select(MathRequest).where(MathRequest.id == request_id)
        result = await self.db.execute(stmt)
        request = result.scalar_one_or_none()
        if request:
            return MathRequestRead.model_validate(request)
        return None

    async def update_request(self, request_id: int, request_data: MathRequestCreate) -> None:
        stmt = select(MathRequest).where(MathRequest.id == request_id)
        result = await self.db.execute(stmt)
        request = result.scalar_one_or_none()
        if request:
            for field, value in request_data.model_dump().items():
                setattr(request, field, value)
            await self.db.commit()

    async def delete_request(self, request_id: int) -> None:
        stmt = select(MathRequest).where(MathRequest.id == request_id)
        result = await self.db.execute(stmt)
        request = result.scalar_one_or_none()

        if request:
            await self.db.delete(request)
            await self.db.commit()