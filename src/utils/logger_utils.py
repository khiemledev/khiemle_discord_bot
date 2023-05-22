import logging
from pathlib import Path


class LoggingFormatter(logging.Formatter):
    # Colors
    black = "\x1b[30m"
    red = "\x1b[31m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    blue = "\x1b[34m"
    gray = "\x1b[38m"
    # Styles
    reset = "\x1b[0m"
    bold = "\x1b[1m"

    COLORS = {
        logging.DEBUG: gray + bold,
        logging.INFO: blue + bold,
        logging.WARNING: yellow + bold,
        logging.ERROR: red,
        logging.CRITICAL: red + bold,
    }

    def format(self, record):
        log_color = self.COLORS[record.levelno]
        format = (
            "(black){asctime}(reset) (levelcolor){levelname:<8}(reset)"
            " (green){name}(reset) {message}"
        )
        format = format.replace("(black)", self.black + self.bold)
        format = format.replace("(reset)", self.reset)
        format = format.replace("(levelcolor)", log_color)
        format = format.replace("(green)", self.green + self.bold)
        formatter = logging.Formatter(format, "%Y-%m-%d %H:%M:%S", style="{")
        return formatter.format(record)


def get_logger(
    name="discord_bot", logfile="logs/discord.py"
) -> logging.Logger:
    """Get logger with console and file handler"""

    # Make sure that log dir is exists
    p = Path(logfile)
    p.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(LoggingFormatter())
    # File handler
    file_handler = logging.FileHandler(
        filename=logfile,
        encoding="utf-8",
        mode="w",
    )
    file_handler_formatter = logging.Formatter(
        "[{asctime}] [{levelname}] {name}[{funcName}({lineno})]: {message}",
        "%Y-%m-%d %H:%M:%S",
        style="{",  # noqa E501
    )
    file_handler.setFormatter(file_handler_formatter)

    # Add the handlers
    if not logger.hasHandlers():
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
