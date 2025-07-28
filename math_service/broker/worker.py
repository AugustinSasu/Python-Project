import aio_pika
import json
from services.math_srv import MathService
from models.MathRequest import MathRequestCreate


class MathWorker:
    def __init__(self, srv: MathService):
        self.service = srv
        self.operations = {
            "power": self.service.power,
            "fibonacci": self.service.fibonacci,
            "factorial": self.service.factorial,
        }

    async def handle_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            try:
                req = MathRequestCreate.model_validate_json(message.body.decode())

                print(f"[TASK RECEIVED] {req.operation}({req.input_data})")

                func = self.operations.get(req.operation)

                if func:
                    result = await func(**request_model.input_data)
                    response = {
                        "status": "success",
                        "operation": operation,
                        "result": result
                    }
                else:
                    response = {
                        "status": "error",
                        "message": f"Unknown operation: {operation}"
                    }

                # ➕ Handle RPC reply
                if message.reply_to and message.correlation_id:
                    response_msg = aio_pika.Message(
                        body=json.dumps(response).encode(),
                        correlation_id=message.correlation_id
                    )
                    await message.channel.default_exchange.publish(
                        response_msg,
                        routing_key=message.reply_to
                    )
                    print(f"[RESPONSE SENT] correlation_id={message.correlation_id}")
                else:
                    print("[INFO] No reply_to or correlation_id found — fire-and-forget mode")

            except Exception as e:
                error_response = {
                    "status": "error",
                    "message": f"Exception: {str(e)}"
                }

                print(f"[ERROR] {str(e)}")

                # Send error response if reply_to is available
                if message.reply_to and message.correlation_id:
                    response_msg = aio_pika.Message(
                        body=json.dumps(error_response).encode(),
                        correlation_id=message.correlation_id
                    )
                    await message.channel.default_exchange.publish(
                        response_msg,
                        routing_key=message.reply_to
                    )
