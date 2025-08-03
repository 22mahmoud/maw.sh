# pyright: reportCallIssue=false
# pyright: reportOptionalSubscript=false
# pyright: reportArgumentType=false
# pyright: reportArgumentType=false
# pyright: reportOperatorIssue=false
# pyright: reportReturnType=false
from datetime import datetime
from logging import LogRecord
from typing import Any

from pythonjsonlogger.json import JsonFormatter


class DjangoJsonRequestFormatter(JsonFormatter):
    def add_fields(
        self,
        log_record: dict[str, Any],
        record: LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)

        log_record["time"] = datetime.fromtimestamp(record.created).isoformat()
        log_record.pop("asctime", None)

        log_record.update(
            {
                "pid": record.process,
                "thread": record.thread,
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName,
                "message": record.getMessage(),
            }
        )


class JsonRequestFormatter(JsonFormatter):
    def add_fields(
        self,
        log_record: dict[str, Any],
        record: LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        args: dict = record.args

        t = args.get("t", "").strip("[]")
        response_time = None

        if t:
            try:
                response_time = datetime.strptime(t, "%d/%b/%Y:%H:%M:%S %z")
            except ValueError as e:
                print(f"Failed to parse timestamp '{t}': {e}")

        url = args.get("U", "")
        if args.get("q"):
            url += f"?{args['q']}"

        log_record.update(
            {
                "remote_ip": args.get("h"),
                "method": args.get("m"),
                "path": url,
                "status": args.get("s"),
                "time": response_time.isoformat() if response_time else None,
                "user_agent": args.get("a"),
                "referer": args.get("f"),
                "duration_in_ms": args.get("M"),
                "pid": args.get("p"),
            }
        )


class JsonErrorFormatter(JsonFormatter):
    def add_fields(
        self,
        log_record: dict[str, Any],
        record: LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record["level"] = log_record.get("levelname", "")
