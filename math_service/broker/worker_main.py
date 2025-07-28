import asyncio
import aio_pika
from broker.worker import MathWorker
from services.math_srv import MathService
from repos.RequestsRepo import RequestsRepo
from database import database  # your DB object

AMQP_URL = "amqp://guest:guest@rabbitmq/"  # 👈 use 'rabbitmq' (service name) inside Docker network
QUEUE_NAME = "math_requests"


async def main():
    await database.connect()

    repo = RequestsRepo(database)
    service = MathService(repo)
    worker = MathWorker(service)

    connection = await aio_pika.connect_robust(AMQP_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)

    queue = await channel.declare_queue(QUEUE_NAME, durable=True)
    await queue.consume(worker.handle_message)

    print(f"[WORKER READY] Listening on queue: {QUEUE_NAME}")
    await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
