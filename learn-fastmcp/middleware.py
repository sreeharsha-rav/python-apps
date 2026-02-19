import sys
import time
import logging
from fastmcp.utilities.logging import get_logger
from fastmcp.server.middleware import Middleware, MiddlewareContext


class ConsoleFormatter(logging.Formatter):
    """
    Custom formatter with colors for specific fields to mimic a production-ready standard output.
    Format: [TIME] [LEVEL] [REQ-ID] [LOGGER] MESSAGE
    """
    # ANSI Color Codes
    GREY = "\x1b[38;20m"
    CYAN = "\x1b[36;20m"
    GREEN = "\x1b[32;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    MAGENTA = "\x1b[35;20m"
    BLUE = "\x1b[34;20m"
    RESET = "\x1b[0m"

    def format(self, record):
        asctime = self.formatTime(record, self.datefmt)
        
        if record.levelno == logging.DEBUG:
            level_color = self.GREY
        elif record.levelno == logging.INFO:
            level_color = self.GREEN
        elif record.levelno == logging.WARNING:
            level_color = self.YELLOW
        elif record.levelno == logging.ERROR:
            level_color = self.RED
        elif record.levelno == logging.CRITICAL:
            level_color = self.BOLD_RED
        else:
            level_color = self.RESET

        # Formatting parts
        time_str = f"{self.CYAN}[{asctime}]{self.RESET}"
        level_str = f"{level_color}[{record.levelname}]{self.RESET}"
        name_str = f"{self.BLUE}[{record.name}]{self.RESET}"
        
        # Message
        message = record.getMessage()
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
            message += f"\n{record.exc_text}"
        
        return f"{time_str} {level_str} {name_str} | {message}"

def configure_logging():
    """
    Configures logging using dictConfig.
    - Disables existing loggers to avoid duplicate/unformatted logs.
    - Sets up a central console handler with the custom formatter.
    - Re-routes uvicorn logs to use this formatter for consistency.
    """
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {},
        "formatters": {
            "default": {
                "()": ConsoleFormatter,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "default",
                "filters": [],
            },
        },
        "loggers": {
            "root": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }
    logging.config.dictConfig(LOGGING_CONFIG)

class LoggingMiddleware(Middleware):
    async def on_message(self, context: MiddlewareContext, call_next):
        """Middleware to log incoming requests and outgoing responses with timing and error handling."""
        start_time = time.time()
        logger = get_logger(__name__)
        
        try:
            logger.info(f"method: {context.method} - source: {context.source} - type: {context.type} - message: {context.message}")
            
            response = await call_next(context)
            
            process_time = (time.time() - start_time) * 1000
            
            logger.info(
                f"Response: {response} "
                f"| Time: {process_time:.2f}ms"
            )
            return response
            
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.error(
                f"Request failed: method: {context.method} - source: {context.source} - type: {context.type} - message: {context.message} "
                f"| Time: {process_time:.2f}ms",
                exc_info=True
            )
            raise e
