import aio_pika
import json

from services.math_srv import MathService
from models.MathRequest import MathRequestCreate
from logging_config import logger


class MathWorker:
    def __init__(self, srv: MathService, channel):
        self.service = srv
        self.channel = channel
        self.operations = {
            "power": self.service.power,
            "fibonacci": self.service.fibonacci,
            "factorial": self.service.factorial,
        }

    async def handle_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                logger.debug(f"[RECEIVED MESSAGE] {message.body.decode()}")
                req = MathRequestCreate.model_validate_json(message.body.decode())

                logger.info(f"[TASK RECEIVED] {req.operation}({req.input_data})")

                func = self.operations.get(req.operation)

                if func:
                    params = json.loads(req.input_data)  # Convert string → dict
                    result = await func(**params)
                    response = {
                        "status": "success",
                        "operation": req.operation,
                        "result": result
                    }
                else:
                    response = {
                        "status": "error",
                        "message": f"Unknown operation: {req.operation}"
                    }

                # ➕ Handle RPC reply
                if message.reply_to and message.correlation_id:
                    response_msg = aio_pika.Message(
                        body=json.dumps(response).encode(),
                        correlation_id=message.correlation_id
                    )
                    await self.channel.default_exchange.publish(
                        response_msg,
                        routing_key=message.reply_to
                    )
                    logger.info(f"[RESPONSE SENT] correlation_id={message.correlation_id}")
                else:
                    logger.info("[INFO] No reply_to or correlation_id found — fire-and-forget mode")

            except Exception as e:
                error_response = {
                    "status": "error",
                    "message": f"Exception: {str(e)}"
                }

                logger.exception("[ERROR] Unexpected exception:")

                # Send error response if reply_to is available
                if message.reply_to and message.correlation_id:
                    response_msg = aio_pika.Message(
                        body=json.dumps(error_response).encode(),
                        correlation_id=message.correlation_id
                    )
                    await self.channel.default_exchange.publish(
                        response_msg,
                        routing_key=message.reply_to
                    )
