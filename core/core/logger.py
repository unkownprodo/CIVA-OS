from dataclasses import dataclass, field
from typing import List, Optional
from time import time
from datetime import datetime


@dataclass
class LogEntry:
    timestamp: float
    command: str
    metadata: Optional[dict] = field(default=None)


class Logger:
    def __init__(self):
        self._entries: List[LogEntry] = []

    def log(self, command: str, metadata: Optional[dict] = None):
        self._entries.append(
            LogEntry(
                timestamp=time(),
                command=command,
                metadata=metadata
            )
        )

    def get_all(self):
        return self._entries

    def clear(self):
        self._entries.clear()

    def format_entries(self):
        """Human-readable syslog output"""
        lines = []
        for i, entry in enumerate(self._entries, 1):
            ts = datetime.fromtimestamp(entry.timestamp).strftime("%H:%M:%S")
            lines.append(f"{i:>3}. [{ts}] {entry.command}")
        return lines