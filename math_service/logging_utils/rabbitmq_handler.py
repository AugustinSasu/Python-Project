# rabbitmq_handler.py to handle logging to RabbitMQ; receives log records from the logger and sends them to a RabbitMQ queue
import logging
# pika is the RabbitMQ client library
import pika
import json


class RabbitMQHandler(logging.Handler):
    def __init__(self, host='localhost', queue='logs'):
        super().__init__()
        self.queue = queue
        self.connection = None
        self.channel = None

        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue, durable=True)
        except Exception as e:
            print(f"[!] Failed to connect RabbitMQ logging handler: {e}")

    def emit(self, record):
        try:
            if self.channel:
                log_entry = self.format(record)
                self.channel.basic_publish(
                    exchange='',
                    routing_key=self.queue,
                    body=json.dumps({"log": log_entry}),
                    properties=pika.BasicProperties(delivery_mode=2)
                )
        except Exception:
            self.handleError(record)

    def close(self):
        try:
            if hasattr(self, "connection") and self.connection:
                self.connection.close()
        finally:
            super().close()