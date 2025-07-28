import asyncio
import aio_pika
from math_service.services.math_srv import MathService
from math_service.repos.RequestsRepo import RequestsRepo
from math_service.broker.worker import MathWorker
from database import database

AMQP_URL = "amqp://guest:guest@localhost/"
QUEUE_NAME = "math_requests"
NUM_WORKERS = 3


async def start_worker(channel, queue_name, worker: MathWorker):
    queue = await channel.declare_queue(queue_name, durable=True)
    await queue.consume(worker.handle_message)
    print(f"🔄 Worker started on queue '{queue_name}'")


async def main():
    # Connect to DB
    await database.connect()
    repo = RequestsRepo(database)
    service = MathService(repo)
    worker = MathWorker(service)

    # Connect to RabbitMQ
    connection = await aio_pika.connect_robust(AMQP_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=NUM_WORKERS)

    # Start multiple consumers (same queue)
    await asyncio.gather(*[
        start_worker(channel, QUEUE_NAME, worker)
        for _ in range(NUM_WORKERS)
    ])

    print(f"✅ Started {NUM_WORKERS} worker consumers")
    await asyncio.Future()  # Keep the process alive


if __name__ == "__main__":
    asyncio.run(main())
