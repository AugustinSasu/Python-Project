import logging
import sys
import time
from logging_utils.rabbitmq_handler import RabbitMQHandler


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno >= logging.ERROR:
            self._style._fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]'
        else:
            self._style._fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        return super().format(record)


logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)


def init_logging(
    rabbit_host: str = "rabbitmq",
    rabbit_queue: str = "logs",
    retries: int = 5,
    delay: float = 2.0,
):
    """
    Call this once (e.g. in FastAPI's startup event) to wire up:
      - RabbitMQHandler (INFO+)
      - console StreamHandler (DEBUG+)
    Includes a simple retry loop for RabbitMQ connectivity.
    """
    # avoid double‐adding if someone calls init_logging twice
    if logger.handlers:
        return

    # 2) Try connecting to RabbitMQ, retrying a few times
    rabbit_handler = None
    for attempt in range(1, retries + 1):
        try:
            rabbit_handler = RabbitMQHandler(host=rabbit_host, queue=rabbit_queue)
            # success → stop retrying
            break
        except Exception as e:
            if attempt == retries:
                # final failure: log to console only
                print(f"[!] RabbitMQ unavailable after {retries} attempts: {e}")
            else:
                time.sleep(delay)

    # 3) If we got a handler, wire it up
    if rabbit_handler:
        rabbit_handler.setLevel(logging.INFO)
        rabbit_handler.setFormatter(CustomFormatter())
        # Add RabbitMQ handler to the logger
        logger.addHandler(rabbit_handler)

    # 4) Always add a console handler for DEBUG+
    console_h = logging.StreamHandler(sys.stdout)
    console_h.setLevel(logging.DEBUG)
    console_h.setFormatter(CustomFormatter())
    logger.addHandler(console_h)
