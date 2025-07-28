# routes/math_routes.py

from fastapi import APIRouter, Query, HTTPException
import uuid
import json
import asyncio
import aio_pika
from models.MathRequest import MathRequestCreate

router = APIRouter()
publisher: aio_pika.RobustConnection = None  # Will be injected


async def rpc_call(operation: str, params: dict, timeout: float = 5.0):
    correlation_id = str(uuid.uuid4())

    # Open a new channel and reply queue
    channel = await publisher.channel()
    callback_queue = await channel.declare_queue(exclusive=True)

    future = asyncio.get_event_loop().create_future()

    async def on_response(message: aio_pika.IncomingMessage):
        async with message.process():
            if message.correlation_id == correlation_id:
                payload = json.loads(message.body.decode())
                future.set_result(payload)

    await callback_queue.consume(on_response)

    request_model = MathRequestCreate(
        operation=operation,
        input_data=json.dumps(params),
    )

    message = aio_pika.Message(
        body=request_model.model_dump_json().encode(),
        correlation_id=correlation_id,
        reply_to=callback_queue.name
    )

    await channel.default_exchange.publish(
        message, routing_key="math_requests"
    )

    try:
        return await asyncio.wait_for(future, timeout)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Timeout waiting for worker response")


@router.get("/pow")
async def power(x: float = Query(...), y: float = Query(...)):
    result = await rpc_call("power", {"x": x, "y": y})
    return result


@router.get("/fib")
async def fib(n: int = Query(...)):
    if n < 0:
        raise HTTPException(status_code=400, detail="n must be >= 0")
    result = await rpc_call("fibonacci", {"n": n})
    return result


@router.get("/factorial")
async def factorial(n: int = Query(...)):
    if n < 0:
        raise HTTPException(status_code=400, detail="n must be >= 0")
    result = await rpc_call("factorial", {"n": n})
    return result
