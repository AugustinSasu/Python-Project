from typing import Optional
from models.MathRequest import MathRequestCreate, MathRequestRead


class RequestsRepo:
    def __init__(self, db):
        self.db = db

    async def get_request(self, request_id: int) -> Optional[MathRequestRead]:
        query = "SELECT * FROM math_requests WHERE id = :id"
        row = await self.db.fetch_one(query, values={"id": request_id})
        if row:
            return MathRequestRead(**row)
        return None

    async def create_request(self, request_data: MathRequestCreate) -> int:
        query = """
            INSERT INTO math_requests (operation, input_data, result)
            VALUES (:operation, :input_data, :result)
            RETURNING id
        """
        values = request_data.dict()
        return await self.db.execute(query=query, values=values)

    async def update_request(
            self, request_id: int,
            request_data: MathRequestCreate) -> None:

        query = """
            UPDATE math_requests
            SET operation = :operation,
                input_data = :input_data,
                result = :result
            WHERE id = :id
        """
        values = request_data.dict()
        values["id"] = request_id
        await self.db.execute(query=query, values=values)

    async def delete_request(self, request_id: int) -> None:
        query = "DELETE FROM math_requests WHERE id = :id"
        await self.db.execute(query=query, values={"id": request_id})
