import json
import logging
import logging.config
from datetime import datetime, timezone
from typing import Literal

from typing_extensions import override

from ..settings import Settings

_LOGGER_NAME = "fast-analytics"

_DEBUG_LOGGER = "fast-analytics.debug"

LOG_RECORD_BUILTIN_ATTRS = {
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "src.entrypoints.logger.JsonFormatter",
            "fmt_json": {
                "level": "levelname",
                "logger": "name",
                "file_name": "filename",
                "function": "funcName",
                "line": "lineno",
                "thread": "threadName",
                "process_name": "processName",
                "process_id": "process",
            },
        },
        "standard": {
            "()": "uvicorn.logging.DefaultFormatter",
            "use_colors": True,
            "format": "%(levelprefix)s[%(name)s|%(process)s] - %(message)s",
        },
    },
    "handlers": {
        "console-standard": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": "ext://sys.stderr",
        },
        "console-json": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        _LOGGER_NAME: {
            "handlers": ["console-json"],
            "propagate": False,
        },
        _DEBUG_LOGGER: {
            "handlers": ["console-json", "console-standard"],
            "propagate": False,
        },
        "sqlalchemy": {"handlers": ["console-json"], "propagate": False},
    },
}


class JsonFormatter(logging.Formatter):
    def __init__(
        self,
        datefmt: str | None = None,
        style: Literal["%", "{", "$"] = "%",
        fmt_json: dict[str, str] | None = None,
    ):
        super().__init__(datefmt=datefmt, style=style)
        self._fmt_json = {}
        for key, value in (fmt_json or {}).items():
            if value not in LOG_RECORD_BUILTIN_ATTRS:
                raise ValueError(f"LogRecord has no attribute '{value}'")
            self._fmt_json[key] = value
        self._fmt_json = fmt_json if fmt_json else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        dict_record = self.__prepare_record(record)
        return json.dumps(dict_record, default=str)

    def __prepare_record(self, record: logging.LogRecord) -> dict:
        created = datetime.fromtimestamp(record.created, timezone.utc)
        dict_record = {
            "level": record.levelname,
            "timestamp": created.isoformat()
            if not self.datefmt
            else created.strftime(self.datefmt),
            "msg": record.getMessage(),
        }
        if record.exc_info:
            dict_record["exec_info"] = self.formatException(record.exc_info)
        if record.stack_info:
            dict_record["stack_info"] = self.formatStack(record.stack_info)

        for key, value in self._fmt_json.items():
            dict_record[key] = getattr(record, value)

        return dict_record


def init_loggers():
    logging.config.dictConfig(LOGGING_CONFIG)
    for logger in logging.root.manager.loggerDict:
        logging.getLogger(logger).setLevel(logging.DEBUG if Settings.debug else logging.INFO)


def get_logger():
    if Settings.debug:
        return logging.getLogger(_DEBUG_LOGGER)
    return logging.getLogger(_LOGGER_NAME)
