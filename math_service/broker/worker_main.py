import asyncio
import aio_pika
from aio_pika.exceptions import AMQPConnectionError
from broker.worker import MathWorker
from services.math_srv import MathService
from repos.RequestsRepo import RequestsRepo
from database import SessionLocal

AMQP_URL = "amqp://guest:guest@rabbitmq/"
QUEUE_NAME = "math_requests"


# wait for RabbitMQ to be ready
async def wait_for_rabbitmq(amqp_url: str, retries: int = 10, delay: float = 2.0):
    for attempt in range(retries):
        try:
            return await aio_pika.connect_robust(amqp_url)
        except AMQPConnectionError:
            print(f"[WARN] RabbitMQ not ready for worker (attempt {attempt + 1}/{retries}), retrying in {delay}s...")
            await asyncio.sleep(delay)
    raise RuntimeError("Failed to connect worker to RabbitMQ after multiple attempts.")


async def main():
    # Start RabbitMQ connection
    connection = await wait_for_rabbitmq(AMQP_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)

    # Create queue
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    # Create DB session
    async with SessionLocal() as session:
        repo = RequestsRepo(session)          # Use SQLAlchemy AsyncSession
        service = MathService(repo)
        worker = MathWorker(service, channel)

        # Bind message handler
        print("About to register consumer...")
        await queue.consume(worker.handle_message)

        print(f"[WORKER READY] Listening on queue: {QUEUE_NAME}")
        await asyncio.Future()  # Keep running forever


if __name__ == "__main__":
    asyncio.run(main())
