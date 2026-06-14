
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from pathlib import Path
from typing import Optional, Union

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
DEFAULT_LOG_DIR: str = "logs"
DEFAULT_LOG_FILE: str = "app.log"
DEFAULT_LOG_LEVEL: str = "INFO"
DEFAULT_LOG_FORMAT: str = (
    "[%(asctime)s] [%(levelname)-8s] [%(name)s:%(lineno)d] %(message)s"
)
DEFAULT_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

DEFAULT_CONSOLE_FORMAT: str = "[%(levelname)-8s] %(name)s — %(message)s"

_handlers_cache: dict = {}


def ensure_log_dir(log_dir: str = DEFAULT_LOG_DIR) -> Path:
    path = Path(log_dir)
    path.mkdir(parents=True, exist_ok=True)
    gitkeep = path / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.touch()
    return path


def _build_file_handler(
    log_path: Union[str, Path],
    level: str = DEFAULT_LOG_LEVEL,
    fmt: Optional[str] = None,
    datefmt: Optional[str] = None,
    when: Optional[str] = None,
    backup_count: int = 30,
    max_bytes: Optional[int] = None,
    encoding: str = "utf-8",
) -> logging.Handler:
    log_path = Path(log_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)  
    formatter = logging.Formatter(
        fmt=fmt or DEFAULT_LOG_FORMAT,
        datefmt=datefmt or DEFAULT_DATE_FORMAT,
    )

    if when: 
        handler = TimedRotatingFileHandler(
            filename=str(log_path),
            when=when,
            interval=1,
            backupCount=backup_count,
            encoding=encoding,
        )
        handler.suffix = "%Y-%m-%d"
    elif max_bytes: 
        handler = RotatingFileHandler(
            filename=str(log_path),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding=encoding,
        )
    else:
        handler = logging.FileHandler(
            filename=str(log_path),
            encoding=encoding,
        )

    handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    handler.setFormatter(formatter)
    return handler


def _build_console_handler(
    level: str = DEFAULT_LOG_LEVEL,
    fmt: Optional[str] = None,
    datefmt: Optional[str] = None,
) -> logging.Handler:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, level.upper(), logging.INFO))
    handler.setFormatter(
        logging.Formatter(
            fmt=fmt or DEFAULT_CONSOLE_FORMAT,
            datefmt=datefmt or DEFAULT_DATE_FORMAT,
        )
    )
    return handler


def setup_logging(
    log_dir: str = DEFAULT_LOG_DIR,
    log_file: str = DEFAULT_LOG_FILE,
    level: str = DEFAULT_LOG_LEVEL,
    console: bool = True,
    file_fmt: Optional[str] = None,
    console_fmt: Optional[str] = None,
    datefmt: Optional[str] = None,
    when: Optional[str] = None,
    backup_count: int = 30,
    max_bytes: Optional[int] = None,
) -> None:
    ensure_log_dir(log_dir)

    log_level = getattr(logging, level.upper(), logging.INFO)
    log_path = Path(log_dir) / log_file

    root = logging.getLogger()
    root.setLevel(log_level)

    root.handlers.clear()

    file_handler = _build_file_handler(
        log_path=log_path,
        level=level,
        fmt=file_fmt,
        datefmt=datefmt,
        when=when,
        backup_count=backup_count,
        max_bytes=max_bytes,
    )
    root.addHandler(file_handler)

    if console:
        console_handler = _build_console_handler(
            level=level,
            fmt=console_fmt,
            datefmt=datefmt,
        )
        root.addHandler(console_handler)

    for lib in ("urllib3", "requests", "matplotlib", "PIL"):
        logging.getLogger(lib).setLevel(logging.WARNING)


def get_logger(
    name: str,
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    log_dir: str = DEFAULT_LOG_DIR,
    console: bool = True,
    when: Optional[str] = None,
    backup_count: int = 30,
    max_bytes: Optional[int] = None,
) -> logging.Logger:

    root = logging.getLogger()
    if not root.handlers:
        setup_logging(
            log_dir=log_dir,
            log_file=DEFAULT_LOG_FILE,
            level=level or DEFAULT_LOG_LEVEL,
            console=console,
            when=when,
            backup_count=backup_count,
            max_bytes=max_bytes,
        )

    logger = logging.getLogger(name)

    if level:
        logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if log_file:
        log_path = Path(log_file)
        cache_key = str(log_path.resolve())
        if cache_key not in _handlers_cache:
            handler = _build_file_handler(
                log_path=log_path,
                level=level or DEFAULT_LOG_LEVEL,
                when=when,
                backup_count=backup_count,
                max_bytes=max_bytes,
            )
            _handlers_cache[cache_key] = handler
        logger.addHandler(_handlers_cache[cache_key])
        logger.propagate = False 

    return logger


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
def create_daily_logger(name: str) -> logging.Logger:
    return get_logger(name, when="D", backup_count=7)


def create_hourly_logger(name: str) -> logging.Logger:
    return get_logger(name, when="H", backup_count=24)



