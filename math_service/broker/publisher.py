# publisher.py
import aio_pika
import json
import asyncio


class Publisher:
    def __init__(self, amqp_url="amqp://guest:guest@rabbitmq/"):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None

    async def connect(self, retries: int = 10, delay: float = 2.0):
        for attempt in range(1, retries + 1):
            try:
                self.connection = await aio_pika.connect_robust(self.amqp_url)
                self.channel = await self.connection.channel()
                await self.channel.set_qos(prefetch_count=10)
                print("[✔] Connected to RabbitMQ.")
                return
            except Exception as e:
                print(f"[⏳] RabbitMQ not ready (attempt {attempt}/{retries}): {e}")
                await asyncio.sleep(delay)
        raise RuntimeError("❌ Failed to connect to RabbitMQ after several attempts.")

    async def send(self, queue_name: str, payload: dict):
        await self.connect()
        message = aio_pika.Message(body=json.dumps(payload).encode())
        await self.channel.default_exchange.publish(message, routing_key=queue_name)
