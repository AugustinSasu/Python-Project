
import aio_pika
import json

from math_service.services.math_srv import MathService


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
                payload = json.loads(message.body.decode())
                operation = payload.get("operation")
                params = payload.get("params", {})

                print(f"[TASK RECEIVED] {operation}({params})")

                func = self.operations.get(operation)

                # Dispatch operation
                if func:
                    result = await func(**params)
                    return {
                        "status": "success",
                        "operation": operation,
                        "result": result
                    }
                else:
                    print(f"[ERROR] Unknown operation: {operation}")
                    return {
                        "status": "error",
                        "message": f"Unknown operation: {operation}"
                    }

            except Exception as e:
                print(f"[ERROR] Failed to handle message: {e}")
                return {
                    "status": "error",
                    "message": f"Failed to handle message: {e}"
                }
