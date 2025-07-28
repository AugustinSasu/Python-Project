import logging
import sys


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno >= logging.ERROR:
            self._style._fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]'
        else:
            self._style._fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        return super().format(record)


logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    # Use stdout for console output
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)

    formatter = CustomFormatter()
    ch.setFormatter(formatter)

    logger.addHandler(ch)
