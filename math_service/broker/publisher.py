# publisher.py
import aio_pika
import json


class Publisher:
    def __init__(self, amqp_url="amqp://guest:guest@localhost/"):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None

    async def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(self.amqp_url)
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=10)

    async def send(self, queue_name: str, payload: dict):
        await self.connect()
        message = aio_pika.Message(body=json.dumps(payload).encode())
        await self.channel.default_exchange.publish(message, routing_key=queue_name)
